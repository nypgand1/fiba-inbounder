# -*- coding: utf-8 -*-
import pandas as pd
from fiba_inbounder.communicator import FibaCommunicator
from fiba_inbounder.formulas import period_time

class FibaGameParser:
    @staticmethod
    def get_game_teams_json_dataframe_v7(event_id, game_unit):
        game_json = FibaCommunicator.get_game_team_stats_v7(event_id, game_unit)
        teams_json = game_json['content']['full']['Competitors']
        
        for t in teams_json:
            t['Stats']['Name'] = t['Name']
            t['Stats']['TeamCode'] = t['TeamCode']
            t['Stats']['Periods'] = t['Periods']
            t['Stats']['TP'] = period_time(len(t['Periods']))

        home_stats_json = teams_json[0]['Stats']
        away_stats_json = teams_json[1]['Stats']
        
        #Oppenent DREB for calculating OREB%
        home_stats_json['OPP_DR'] = away_stats_json['DR']
        away_stats_json['OPP_DR'] = home_stats_json['DR']

        df = pd.DataFrame([home_stats_json, away_stats_json])
        return game_json, df
