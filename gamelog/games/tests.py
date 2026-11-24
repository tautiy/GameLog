from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch, MagicMock

from .models import (
    Genre, Developer, Publisher, Platform,
    Game, GamePublisher, UserGame, Wishlist, UserGameRating,
)
from .services import search_games, get_game_details, discover_games


class GenreModelTest(TestCase):
    def test_str(self):
        genre = Genre.objects.create(name='Экшн')
        self.assertEqual(str(genre), 'Экшн')


class DeveloperModelTest(TestCase):
    def test_str(self):
        dev = Developer.objects.create(name='CD Projekt RED')
        self.assertEqual(str(dev), 'CD Projekt RED')


class PublisherModelTest(TestCase):
    def test_str(self):
        pub = Publisher.objects.create(name='505 Games')
        self.assertEqual(str(pub), '505 Games')


class PlatformModelTest(TestCase):
    def test_str(self):
        platform = Platform.objects.create(name='PC')
        self.assertEqual(str(platform), 'PC')


class GameModelTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(title='Cyberpunk 2077')

    def test_str(self):
        self.assertEqual(str(self.game), 'Cyberpunk 2077')

    def test_genre_many_to_many(self):
        genre = Genre.objects.create(name='Ролевые игры')
        self.game.genre.add(genre)
        self.assertIn(genre, self.game.genre.all())


class UserGameModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.user_game = UserGame.objects.create(
            user=self.user,
            rawg_id=12345,
            title='Test Game',
            status='playing',
        )

    def test_str(self):
        expected = f'{self.user.username} — Test Game (Играю)'
        self.assertEqual(str(self.user_game), expected)

    def test_unique_together(self):
        with self.assertRaises(Exception):
            UserGame.objects.create(
                user=self.user,
                rawg_id=12345,
                title='Duplicate',
                status='planned',
            )


class WishlistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='wishuser', password='pass123')
        self.item = Wishlist.objects.create(
            user=self.user,
            rawg_id=67890,
            title='Wish Game',
        )

    def test_str(self):
        expected = f'{self.user.username} — Wish Game'
        self.assertEqual(str(self.item), expected)


class UserGameRatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rater', password='pass123')
        self.rating = UserGameRating.objects.create(
            user=self.user,
            rawg_id=11111,
            title='Rated Game',
            rating=5,
            review='Отличная игра!',
        )

    def test_str(self):
        expected = f'{self.user.username} — Rated Game (5)'
        self.assertEqual(str(self.rating), expected)



class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', password='pass123')

    def test_game_list_status(self):
        url = reverse('game_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_list.html')

    def test_game_search_status(self):
        url = reverse('game_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_search.html')

    def test_user_library_requires_login(self):
        url = reverse('user_library')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')

    def test_user_library_authenticated(self):
        self.client.login(username='viewuser', password='pass123')
        url = reverse('user_library')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/user_library.html')

    def test_register_view_status(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/register.html')

    def test_rate_game_requires_login(self):
        url = reverse('rate_game', args=[123])
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')

    def test_recommended_games_requires_login(self):
        url = reverse('recommended_games')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')

    def test_recommended_games_authenticated_empty(self):
        self.client.login(username='viewuser', password='pass123')
        url = reverse('recommended_games')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/recommendations.html')
        self.assertEqual(len(response.context['recommended']), 0)


class ServicesTest(TestCase):
    @patch('games.services.requests.get')
    def test_search_games_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'count': 1,
            'results': [{'id': 1, 'name': 'Test Game', 'rating': 4.5}],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = search_games('test')

        self.assertIsNotNone(result)
        self.assertEqual(result['count'], 1)
        mock_get.assert_called_once()

    @patch('games.services.requests.get')
    def test_search_games_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException('API down')

        result = search_games('test')

        self.assertIsNone(result)

    @patch('games.services.requests.get')
    def test_get_game_details_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 1,
            'name': 'Detail Game',
            'released': '2020-01-01',
            'rating': 4.0,
            'description': '<p>Описание</p>',
            'genres': [{'slug': 'action', 'name': 'Экшн'}],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_game_details(1)

        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Detail Game')

    @patch('games.services.requests.get')
    def test_discover_games_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'count': 2,
            'results': [
                {'id': 1, 'name': 'Game 1', 'rating': 4.8},
                {'id': 2, 'name': 'Game 2', 'rating': 4.5},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = discover_games(genre='action', page_size=5)

        self.assertIsNotNone(result)
        self.assertEqual(result['count'], 2)
        self.assertEqual(len(result['results']), 2)

    @patch('games.services.requests.get')
    def test_discover_games_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException('API down')

        result = discover_games(genre='action')

        self.assertIsNone(result)


class ToggleStatusTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='toggleuser', password='pass123')
        self.client.login(username='toggleuser', password='pass123')

    def test_toggle_user_game_status_add(self):
        url = reverse('toggle_user_game_status', args=[99999])
        response = self.client.post(url, {'status': 'planned'})
        self.assertRedirects(response, reverse('user_library'))
        self.assertTrue(
            UserGame.objects.filter(user=self.user, rawg_id=99999, status='planned').exists()
        )

    def test_toggle_user_game_status_update(self):
        UserGame.objects.create(
            user=self.user, rawg_id=99999, title='Existing', status='planned'
        )
        url = reverse('toggle_user_game_status', args=[99999])
        response = self.client.post(url, {'status': 'completed'})
        self.assertRedirects(response, reverse('user_library'))
        ug = UserGame.objects.get(user=self.user, rawg_id=99999)
        self.assertEqual(ug.status, 'completed')

    def test_remove_user_game(self):
        UserGame.objects.create(
            user=self.user, rawg_id=99999, title='To Remove', status='planned'
        )
        url = reverse('remove_user_game', args=[99999])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('user_library'))
        self.assertFalse(
            UserGame.objects.filter(user=self.user, rawg_id=99999).exists()
        )

    def test_toggle_wishlist_add(self):
        url = reverse('toggle_wishlist', args=[55555])
        response = self.client.post(url)
        self.assertTrue(
            Wishlist.objects.filter(user=self.user, rawg_id=55555).exists()
        )

    def test_toggle_wishlist_remove(self):
        Wishlist.objects.create(user=self.user, rawg_id=55555, title='Wish')
        url = reverse('toggle_wishlist', args=[55555])
        response = self.client.post(url)
        self.assertFalse(
            Wishlist.objects.filter(user=self.user, rawg_id=55555).exists()
        )


class RatingViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='ratinguser', password='pass123')
        self.client.login(username='ratinguser', password='pass123')

    @patch('games.views.get_game_details')
    def test_rate_game_get(self, mock_get_game):
        mock_get_game.return_value = {
            'id': 77777,
            'name': 'Rate Me',
            'released': '2021-01-01',
            'rating': 4.2,
            'description': 'desc',
            'background_image': '',
        }
        url = reverse('rate_game', args=[77777])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/rate_game.html')
        self.assertContains(response, 'Rate Me')

    @patch('games.views.get_game_details')
    def test_rate_game_post_create(self, mock_get_game):
        mock_get_game.return_value = {
            'id': 77778,
            'name': 'New Rated',
            'released': '2021-02-01',
            'rating': 4.0,
            'description': 'desc',
            'background_image': '',
        }
        url = reverse('rate_game', args=[77778])
        response = self.client.post(url, {'rating': 5, 'review': 'Супер!'})
        self.assertRedirects(response, reverse('rawg_game_detail', args=[77778]))
        self.assertTrue(
            UserGameRating.objects.filter(
                user=self.user, rawg_id=77778, rating=5, review='Супер!'
            ).exists()
        )

    @patch('games.views.get_game_details')
    def test_delete_rating(self, mock_get_game):
        mock_get_game.return_value = {'id': 77779, 'name': 'To Delete'}
        UserGameRating.objects.create(
            user=self.user, rawg_id=77779, title='To Delete', rating=3
        )
        url = reverse('delete_rating', args=[77779])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('rawg_game_detail', args=[77779]))
        self.assertFalse(
            UserGameRating.objects.filter(user=self.user, rawg_id=77779).exists()
        )
