
import logging

import requests

from django.conf import settings


RAWG_API_URL = 'https://api.rawg.io/api'

logger = logging.getLogger(__name__)


def search_games(query, genre=None, platform=None, year=None):
    try:
        params = {
            'key': settings.RAWG_API_KEY,
            'search': query,
            'page_size': 10,
        }
        if genre:
            params['genres'] = genre
        if platform:
            params['platforms'] = platform
        if year:
            params['dates'] = f'{year}-01-01,{year}-12-31'

        response = requests.get(
            f'{RAWG_API_URL}/games',
            params=params,
            timeout=(5, 30),
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.error('RAWG search_games error: %s', exc)
        return None


def get_genres():
    try:
        response = requests.get(
            f'{RAWG_API_URL}/genres',
            params={
                'key': settings.RAWG_API_KEY,
            },
            timeout=(5, 30),
        )
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as exc:
        logger.error('RAWG get_genres error: %s', exc)
        return []


def get_platforms():
    try:
        response = requests.get(
            f'{RAWG_API_URL}/platforms',
            params={
                'key': settings.RAWG_API_KEY,
            },
            timeout=(5, 30),
        )
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as exc:
        logger.error('RAWG get_platforms error: %s', exc)
        return []


def discover_games(genre=None, platform=None, year=None, page_size=10):
    """Поиск игр без текстового запроса (подборка по фильтрам)."""
    try:
        params = {
            'key': settings.RAWG_API_KEY,
            'page_size': page_size,
            'ordering': '-rating',
        }
        if genre:
            params['genres'] = genre
        if platform:
            params['platforms'] = platform
        if year:
            params['dates'] = f'{year}-01-01,{year}-12-31'

        response = requests.get(
            f'{RAWG_API_URL}/games',
            params=params,
            timeout=(5, 30),
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.error('RAWG discover_games error: %s', exc)
        return None


def get_game_details(game_id):
    try:
        response = requests.get(
            f'{RAWG_API_URL}/games/{game_id}',
            params={
                'key': settings.RAWG_API_KEY,
            },
            timeout=(5, 30),
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.error('RAWG get_game_details error: %s', exc)
        return None
