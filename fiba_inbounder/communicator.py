# -*- coding: utf-8 -*-
import requests
from fiba_inbounder.settings import LOGGER
from fiba_inbounder.settings import FIBA_DATA_URL_V5, FIBA_GAME_STATS_URL_V7, \
        FIBA_PLAY_BY_PLAY_URL_V7, FIBA_DETAIL_URL_V7, \
        PLEAGUE_GAME_STATS_URL, PLEAGUE_SUB_URL, PLEAGUE_PLAY_BY_PLAY_URL

class FibaCommunicator:
    @staticmethod
    def get(url, params=None, **kwargs):
        r = requests.get(url, params, **kwargs)
        LOGGER.info('{r} GET {url}'.format(r=r, url=url))
        return r

    @staticmethod
    def get_pleague(url, params=dict(), headers=dict(), **kwargs):
        params['key'] = 'AIzaSyDjhn-pYe0kzgyez6RPNKUDXqWEhh_VwZ8'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

        r = requests.get(url, params=params, headers=headers, **kwargs)
        LOGGER.info('{r} GET {url}'.format(r=r, url=url))
        return r

    @staticmethod
    def get_game_data_v5(match_id):
        url = FIBA_DATA_URL_V5.format(match_id=match_id)
        r = FibaCommunicator.get(url)
        return r.json()

    @staticmethod
    def get_game_stats_v7(event_id, game_unit):
        url = FIBA_GAME_STATS_URL_V7.format(event_id=event_id, game_unit=game_unit)
        r = FibaCommunicator.get(url)
        return r.json()

    @staticmethod
    def get_game_play_by_play_v7(event_id, game_unit, period_id):
        url = FIBA_PLAY_BY_PLAY_URL_V7.format(event_id=event_id, game_unit=game_unit, period_id=period_id)
        r = FibaCommunicator.get(url)
        return r.json()

    @staticmethod
    def get_game_details_v7(event_id, game_unit):
        url = FIBA_DETAIL_URL_V7.format(event_id=event_id, game_unit=game_unit)
        r = FibaCommunicator.get(url)
        return r.json()

    @staticmethod
    def get_game_stats_pleague(game_id):
        url = PLEAGUE_GAME_STATS_URL.format(game_id=game_id)
        r = FibaCommunicator.get_pleague(url)
        return r.json()

    @staticmethod
    def get_game_sub_pleague(game_id, team_id):
        url = PLEAGUE_SUB_URL.format(game_id=game_id, team_id=team_id)
        r = FibaCommunicator.get_pleague(url)
        return r.json()

    @staticmethod
    def get_game_play_by_play_pleague(game_id, team_id):
        url = PLEAGUE_PLAY_BY_PLAY_URL.format(game_id=game_id, team_id=team_id)
        r = FibaCommunicator.get_pleague(url)
        return r.json()
