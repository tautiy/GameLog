
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Game, UserGame, Wishlist
from .services import search_games, get_game_details


def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'games/game_detail.html', {'game': game})


def game_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    api_error = False

    if query:
        data = search_games(query)
        if data is None:
            api_error = True
        else:
            results = data.get('results', [])

    return render(
        request,
        'games/game_search.html',
        {
            'query': query,
            'results': results,
            'api_error': api_error,
        }
    )


def rawg_game_detail(request, game_id):
    game = get_game_details(game_id)

    if game is None:
        messages.error(request, 'Не удалось загрузить информацию об игре. Попробуйте позже.')
        return redirect('game_search')

    return render(
        request,
        'games/rawg_game_detail.html',
        {'game': game}
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
