# -*- coding: utf-8 -*-
import requests
from settings import LOGGER
from settings import FIBA_URL

class FibaCommunicator:
    @staticmethod
    def get(url, *args):
        r = requests.get(url, args)
        LOGGER.info('%s GET %s' % (r, url))
        return r

    @staticmethod
    def get_game(game_id):
        url = FIBA_URL.format(game_id=game_id)
        r = FibaCommunicator.get(url)
        return r.json()
