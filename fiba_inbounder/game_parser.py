# -*- coding: utf-8 -*-
import pandas as pd
from fiba_inbounder.communicator import FibaCommunicator
from fiba_inbounder.formulas import game_time, update_xy_v7, update_zone, update_range

class FibaGameParser:
    @staticmethod
    def get_game_teams_json_dataframe_v7(event_id, game_unit):
        game_json = FibaCommunicator.get_game_team_stats_v7(event_id, game_unit)
        team_stats_json = game_json['content']['full']['Competitors']
        
        for t in team_stats_json:
            t['Stats']['Name'] = t['Name']
            t['Stats']['TeamCode'] = t['TeamCode']
            t['Stats']['Periods'] = t['Periods']
            t['Stats']['PeriodIdList'] = [p['Id'] for p in t['Periods']]
            t['Stats']['TP'] = 5 * game_time(len(t['Periods']))

        home_stats_json = team_stats_json[0]['Stats']
        away_stats_json = team_stats_json[1]['Stats']
        
        #Oppenent DREB for calculating OREB%
        home_stats_json['OPP_DR'] = away_stats_json['DR']
        away_stats_json['OPP_DR'] = home_stats_json['DR']

        df = pd.DataFrame([home_stats_json, away_stats_json])
        return df

    @staticmethod
    def get_game_play_by_play_dataframe_v7(event_id, game_unit, period_id_list):
        play_by_play_json = [
            FibaCommunicator.get_game_play_by_play_v7(event_id, game_unit, p)['content']['full']['Items']
            for p in period_id_list]

        df = pd.DataFrame(sum(play_by_play_json, []))
        update_xy_v7(df)
        return df
