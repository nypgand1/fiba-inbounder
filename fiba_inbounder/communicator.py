# -*- coding: utf-8 -*-
import requests
from settings import LOGGER
from settings import FIBA_DATA_URL_V5, FIBA_TEAM_STATS_URL_V7, \
        FIBA_PLAY_BY_PLAY_URL_V7, FIBA_DETAIL_URL_V7

class FibaCommunicator:
    @staticmethod
    def get(url, *args):
        r = requests.get(url, args)
        LOGGER.info('{r} GET {url}'.format(r=r, url=url))
        return r

    @staticmethod
    def get_game_data_v5(match_id):
        url = FIBA_DATA_URL_V5.format(match_id=match_id)
        r = FibaCommunicator.get(url)
        return r.json()

    @staticmethod
    def get_game_team_stats_v7(event_id, game_unit):
        url = FIBA_TEAM_STATS_URL_V7.format(event_id=event_id, game_unit=game_unit)
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
