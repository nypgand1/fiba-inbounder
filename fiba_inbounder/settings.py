# -*- coding: utf-8 -*- 
import logging

LOGGER_FORMAT = '%(levelname)s: %(asctime)-15s: %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger('FibaInbounder')

FIBA_DATA_URL_V5 = 'https://www.fibalivestats.com/data/{match_id}/data.json'

FIBA_TEAM_STATS_URL_V7 = 'https://livecache.sportresult.com/node/db/FIBASTATS_PROD/{event_id}_GAME_{game_unit}_JSON.json'
FIBA_PLAY_BY_PLAY_URL_V7 = 'https://livecache.sportresult.com/node/db/FIBASTATS_PROD/{event_id}_GAMEACTIONS_{game_unit}_{period}_JSON.json'
