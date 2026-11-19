
import logging

import requests

from django.conf import settings


RAWG_API_URL = 'https://api.rawg.io/api'

logger = logging.getLogger(__name__)


def search_games(query):
    try:
        response = requests.get(
            f'{RAWG_API_URL}/games',
            params={
                'key': settings.RAWG_API_KEY,
                'search': query,
                'page_size': 10,
            },
            timeout=(5, 30),
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.error('RAWG search_games error: %s', exc)
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
