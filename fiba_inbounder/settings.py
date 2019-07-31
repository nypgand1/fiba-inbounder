# -*- coding: utf-8 -*- 
import logging

LOGGER_FORMAT = '%(levelname)s: %(asctime)-15s: %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger('FibaInbounder')

FIBA_URL = 'https://www.fibalivestats.com/data/{game_id}/data.json'
