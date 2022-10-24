# -*- coding: utf-8 -*-
import requests
from fiba_inbounder.settings import LOGGER
from fiba_inbounder.settings import FIBA_DATA_URL_V5, FIBA_GAME_STATS_URL_V7, \
        FIBA_PLAY_BY_PLAY_URL_V7, FIBA_DETAIL_URL_V7, \
        PLEAGUE_GAME_STATS_URL, PLEAGUE_SUB_URL, PLEAGUE_PLAY_BY_PLAY_URL
from fiba_inbounder.settings_synergy import SYNERGY_TOKEN_URL, \
        SYNERGY_PLAY_BY_PLAY_URL, SYNERGY_PLAYER_STATS_URL, \
        SYNERGY_CREDENTIAL_ID, SYNERGY_CREDENTIAL_SECRET, SYNERGY_BEARER, \
        SYNERGY_ORGANIZATION_ID

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers['authorization'] = 'Bearer ' + self.token
        return r

class FibaCommunicator:
    @staticmethod
    def get(url, params=None, headers=dict(), **kwargs):
        r = requests.get(url, params, **kwargs)
        LOGGER.info('{r} GET {url}'.format(r=r, url=url))
        return r

    @staticmethod
    def post_synergy_for_token():
        url = SYNERGY_TOKEN_URL
        r = requests.post(url, json={
                'credentialId': SYNERGY_CREDENTIAL_ID,
                'credentialSecret': SYNERGY_CREDENTIAL_SECRET,
                'sport': 'basketball',
                'organization': {'id': [SYNERGY_ORGANIZATION_ID]},
                'scopes': ['read:organization', 'read:organization_live']
            }
        )
        LOGGER.info('{r} POST {url}'.format(r=r, url=url))
        return r

    @staticmethod
    def get_synergy(url, params=dict(), headers=dict(), **kwargs):
        global SYNERGY_BEARER
        r = FibaCommunicator.get(url, params=params, headers=headers, auth=BearerAuth(SYNERGY_BEARER), **kwargs)

        if r.status_code == requests.codes.forbidden:
            SYNERGY_BEARER = FibaCommunicator.post_synergy_for_token().json().get('data', {}).get('token')
            r = FibaCommunicator.get(url, params=params, headers=headers, auth=BearerAuth(SYNERGY_BEARER), **kwargs)

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

    @staticmethod
    def get_game_player_stats_synergy(org_id, game_id):
        url = SYNERGY_PLAYER_STATS_URL.format(organizationId=org_id, fixtureId=game_id)
        params = {'limit': 1000, 'isPlayer': 'true'}
        r = FibaCommunicator.get_synergy(url, params=params)
        return r.json()

    @staticmethod
    def get_game_play_by_play_synergy(org_id, game_id, period_id):
        url = SYNERGY_PLAY_BY_PLAY_URL.format(organizationId=org_id, fixtureId=game_id)
        params = {'periodId': period_id}
        r = FibaCommunicator.get_synergy(url, params=params)
        return r.json()
