# -*- coding: utf-8 -*-
import pandas as pd
from fiba_inbounder.communicator import FibaCommunicator
from fiba_inbounder.formulas import game_time, update_secs_v7, update_xy_v7, update_stats_v7

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

        team_a_stats_json = team_stats_json[0]['Stats']
        team_b_stats_json = team_stats_json[1]['Stats']
       
        team_a_player_stats_list = [p['Stats'] for p in team_stats_json[0]['Children']]
        team_b_player_stats_list = [p['Stats'] for p in team_stats_json[1]['Children']]

        #Oppenent DREB for calculating OREB%
        team_a_stats_json['OPP_DR'] = team_b_stats_json['DR']
        team_b_stats_json['OPP_DR'] = team_a_stats_json['DR']

        team_stats_df = pd.DataFrame([team_a_stats_json, team_b_stats_json])
        player_stats_df = pd.DataFrame(team_a_player_stats_list + team_b_player_stats_list)
        update_secs_v7(player_stats_df)

        return team_stats_df, player_stats_df

    @staticmethod
    def get_game_play_by_play_dataframe_v7(event_id, game_unit, period_id_list):
        pbp_json_list = [
            FibaCommunicator.get_game_play_by_play_v7(event_id, game_unit, p)['content']['full']['Items']
            for p in period_id_list]

        df = pd.DataFrame(sum(pbp_json_list, []))
        update_xy_v7(df)
        update_stats_v7(df)
        return df

    @staticmethod
    def get_game_details_dict_v7(event_id, game_unit):
        dtl_dict = FibaCommunicator.get_game_details_v7(event_id, game_unit)['content']['full']['Competitors']

        id_table = {k: ((v['TeamCode']) if v['IsTeam'] else (v['FirstNameShort']+v['Name']))
                for k, v in dtl_dict.iteritems()}

        all_starters = [v['Id'] for v in dtl_dict.itervalues() if v['Starter']]
        all_teams = [v['Id'] for v in sorted(dtl_dict.itervalues(), cmp=lambda x,y: cmp(x['Order'], y['Order'])) if v['IsTeam']]
       
        starter_dict = dict()
        starter_dict[all_teams[0]] = {v['Id'] for v in dtl_dict.itervalues() 
            if (not v['IsTeam']) and v['Starter'] and v['ParentId']==all_teams[0]}
        starter_dict[all_teams[1]] = {v['Id'] for v in dtl_dict.itervalues() 
            if (not v['IsTeam']) and v['Starter'] and v['ParentId']==all_teams[1]}

        return id_table, starter_dict
