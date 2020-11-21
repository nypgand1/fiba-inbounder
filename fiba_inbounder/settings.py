# -*- coding: utf-8 -*- 
import simplejson
import logging
from fiba_inbounder.shot_chart_zone import SHOT_CHART_ZONE_GEO

LOGGER_FORMAT = '%(levelname)s: %(asctime)-15s: %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger('FibaInbounder')

FIBA_DATA_URL_V5 = 'https://www.fibalivestats.com/data/{match_id}/data.json'

FIBA_GAME_STATS_URL_V7 = 'https://livecache.sportresult.com/node/db/FIBASTATS_PROD/{event_id}_GAME_{game_unit}_JSON.json'
FIBA_PLAY_BY_PLAY_URL_V7 = 'https://livecache.sportresult.com/node/db/FIBASTATS_PROD/{event_id}_GAMEACTIONS_{game_unit}_{period_id}_JSON.json'
FIBA_DETAIL_URL_V7 = 'https://livecache.sportresult.com/node/db/FIBASTATS_PROD/{event_id}_COMPDETAILS_{game_unit}_JSON.json'

PLEAGUE_GAME_STATS_URL = 'http://api.pleagueplus.meetagile.com/rest/game/{game_id}'
PLEAGUE_SUB_URL = 'http://api.pleagueplus.meetagile.com/rest/gameplayerplaytime/{game_id}/{team_id}'

REG_FULL_GAME_MINS = 40

SHOT_CHART_BACKGROUND = 'shotchart_background_zone_652.png'
SHOT_CHART_PERC_RED = [
    0.5, #At Rim
    0.5, 0.5, 0.5, #Mid Two
    0.5, 0.5, 0.5, 0.5, 0.5, #Long Two
    0.333, 0.333, 0.333, 0.333, 0.333 #Three
]
