
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Game, UserGame, Wishlist, UserGameRating
from .forms import UserGameRatingForm
from .services import search_games, get_game_details, get_genres, get_platforms, discover_games


def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'games/game_detail.html', {'game': game})


def game_search(request):
    query = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '').strip()
    platform = request.GET.get('platform', '').strip()
    year = request.GET.get('year', '').strip()

    results = []
    api_error = False

    if query:
        data = search_games(
            query,
            genre=genre or None,
            platform=platform or None,
            year=year or None,
        )
        if data is None:
            api_error = True
        else:
            results = data.get('results', [])

    genres = get_genres()
    platforms = get_platforms()

    years = list(range(2020, 2027))

    return render(
        request,
        'games/game_search.html',
        {
            'query': query,
            'genre': genre,
            'platform': platform,
            'year': year,
            'results': results,
            'api_error': api_error,
            'genres': genres,
            'platforms': platforms,
            'years': years,
        },
    )


def rawg_game_detail(request, game_id):
    game = get_game_details(game_id)

    if game is None:
        messages.error(request, 'Не удалось загрузить информацию об игре. Попробуйте позже.')
        return redirect('game_search')

    user_rating = None
    if request.user.is_authenticated:
        user_rating = UserGameRating.objects.filter(
            user=request.user, rawg_id=game_id
        ).first()

    return render(
        request,
        'games/rawg_game_detail.html',
        {
            'game': game,
            'user_rating': user_rating,
        },
    )


@login_required
def user_library(request):
    user_games = UserGame.objects.filter(user=request.user)
    return render(request, 'games/user_library.html', {'user_games': user_games})


@login_required
def toggle_user_game_status(request, rawg_id):
    if request.method != 'POST':
        return redirect('game_search')

    status = request.POST.get('status')
    valid_statuses = dict(UserGame.STATUS_CHOICES).keys()

    if status not in valid_statuses:
        messages.error(request, 'Некорректный статус игры.')
        return redirect('game_search')

    user_game, created = UserGame.objects.update_or_create(
        user=request.user,
        rawg_id=rawg_id,
        defaults={'status': status},
    )

    action = 'добавлена' if created else 'обновлена'
    messages.success(request, f'Игра {action} в вашу библиотеку со статусом "{user_game.get_status_display()}".')
    return redirect('user_library')


@login_required
def remove_user_game(request, rawg_id):
    UserGame.objects.filter(user=request.user, rawg_id=rawg_id).delete()
    messages.success(request, 'Игра удалена из вашей библиотеки.')
    return redirect('user_library')


@login_required
def toggle_wishlist(request, rawg_id):
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        rawg_id=rawg_id,
    )

    if not created:
        wishlist_item.delete()
        messages.info(request, 'Игра удалена из списка желаемого.')
    else:
        messages.success(request, 'Игра добавлена в список желаемого.')

    return redirect(request.META.get('HTTP_REFERER', 'game_search'))


@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'games/wishlist.html', {'wishlist': wishlist})


from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'games/register.html'
    success_url = reverse_lazy('game_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        from django.contrib.auth import login
        login(self.request, self.object)
        from django.contrib import messages
        messages.success(self.request, 'Регистрация успешна! Добро пожаловать в GameLog.')
        return response


@login_required
def rate_game(request, rawg_id):
    game_data = get_game_details(rawg_id)
    if game_data is None:
        messages.error(request, 'Не удалось загрузить информацию об игре. Попробуйте позже.')
        return redirect('game_search')

    rating_qs = UserGameRating.objects.filter(user=request.user, rawg_id=rawg_id)
    existing = rating_qs.first()

    if request.method == 'POST':
        form = UserGameRatingForm(request.POST, instance=existing)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.rawg_id = rawg_id
            rating.title = game_data.get('name', '')
            rating.save()
            action = 'обновлена' if existing else 'добавлена'
            messages.success(request, f'Оценка {action} для игры "{rating.title}".')
            return redirect('rawg_game_detail', game_id=rawg_id)
    else:
        form = UserGameRatingForm(instance=existing)

    return render(
        request,
        'games/rate_game.html',
        {
            'form': form,
            'game': game_data,
            'existing_rating': existing,
        },
    )


@login_required
def delete_rating(request, rawg_id):
    if request.method != 'POST':
        return redirect('rawg_game_detail', game_id=rawg_id)

    deleted, _ = UserGameRating.objects.filter(
        user=request.user, rawg_id=rawg_id
    ).delete()
    if deleted:
        messages.success(request, 'Ваша оценка и рецензия удалены.')
    else:
        messages.info(request, 'У вас нет оценки для этой игры.')
    return redirect('rawg_game_detail', game_id=rawg_id)


@login_required
def recommended_games(request):
    user_games = UserGame.objects.filter(user=request.user)
    seen_rawg_ids = set(user_games.values_list('rawg_id', flat=True))

    # Собираем жанры из игр со статусом "Играю" или "Пройдено"
    genre_counts = {}
    for ug in user_games.filter(status__in=('playing', 'completed')):
        data = get_game_details(ug.rawg_id)
        if data:
            for g in data.get('genres', []):
                genre_counts[g['slug']] = genre_counts.get(g['slug'], 0) + 1

    top_genres = sorted(genre_counts, key=genre_counts.get, reverse=True)[:3]

    recommended = []
    for slug in top_genres:
        data = discover_games(genre=slug, page_size=8)
        if data:
            for game in data.get('results', []):
                if game['id'] not in seen_rawg_ids:
                    recommended.append(game)
                    seen_rawg_ids.add(game['id'])
                if len(recommended) >= 12:
                    break
        if len(recommended) >= 12:
            break

    return render(
        request,
        'games/recommendations.html',
        {
            'recommended': recommended,
            'top_genres': top_genres,
        },
    )
