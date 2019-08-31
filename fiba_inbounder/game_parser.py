# -*- coding: utf-8 -*-
import pandas as pd
from fiba_inbounder.communicator import FibaCommunicator
from fiba_inbounder.formulas import game_time, update_secs_v7, update_xy_v7, update_zone, update_range

class FibaGameParser:
    @staticmethod
    def get_game_stats_dataframe_v7(event_id, game_unit):
        game_json = FibaCommunicator.get_game_team_stats_v7(event_id, game_unit)
        team_stats_json = game_json['content']['full']['Competitors']

        for t in team_stats_json:
            #Team Stats
            t['Stats']['Name'] = t['Name']
            t['Stats']['TeamCode'] = t['TeamCode']
            t['Stats']['Periods'] = t['Periods']
            t['Stats']['PeriodIdList'] = [p['Id'] for p in t['Periods']]
            t['Stats']['TP'] = 5 * game_time(len(t['Periods']))
    
            #Player Stats
            for p in t['Children']:
                p['Stats']['TeamCode'] = t['TeamCode']
                p['Stats']['TeamId'] = t['Id']
                p['Stats']['JerseyNumber'] = p['JerseyNumber']
                p['Stats']['Name'] = p['Name']

        home_team_stats_json = team_stats_json[0]['Stats']
        away_team_stats_json = team_stats_json[1]['Stats']
       
        home_player_stats_list = [p['Stats'] for p in team_stats_json[0]['Children']]
        away_player_stats_list = [p['Stats'] for p in team_stats_json[1]['Children']]

        #Oppenent DREB for calculating OREB%
        home_team_stats_json['OPP_DR'] = away_team_stats_json['DR']
        away_team_stats_json['OPP_DR'] = home_team_stats_json['DR']

        team_stats_df = pd.DataFrame([home_team_stats_json, away_team_stats_json])
        player_stats_df = pd.DataFrame(home_player_stats_list + away_player_stats_list)
        update_secs_v7(player_stats_df)

        return team_stats_df, player_stats_df

    @staticmethod
    def get_game_play_by_play_dataframe_v7(event_id, game_unit, period_id_list):
        pbp_json_list = [
            FibaCommunicator.get_game_play_by_play_v7(event_id, game_unit, p)['content']['full']['Items']
            for p in period_id_list]

        df = pd.DataFrame(sum(pbp_json_list, []))
        update_xy_v7(df)
        return df

    @staticmethod
    def get_game_details_v7(event_id, game_unit):
        dtl_dict = FibaCommunicator.get_game_details_v7(event_id, game_unit)['content']['full']['Competitors']

        id_table = {k: ((v['TeamCode']) if v['IsTeam'] else (v['FirstNameShort']+v['Name']))
                for k, v in dtl_dict.iteritems()}

        starters_dict = dict()
        for t in [k for k, v in dtl_dict.iteritems() if v['IsTeam']]:
            starters_dict[t] = [k for k, v in dtl_dict.iteritems() 
                    if (not v['IsTeam']) and v['Starter'] and v['ParentId']==t]

        return id_table, starters_dict
