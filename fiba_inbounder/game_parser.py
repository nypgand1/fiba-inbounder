# -*- coding: utf-8 -*-
import pandas as pd
import fiba_inbounder.formulas
from fiba_inbounder.communicator import FibaCommunicator
from fiba_inbounder.converter import game_time, base60_from, base60_to, \
        convert_team_stats_v5_to_v7, convert_player_stats_v5_to_v7, \
        convert_team_stats_pleague_to_v7, convert_player_stats_pleague_to_v7, \
        convert_secs_v7, convert_xy_v7, convert_xy_v5, \
        convert_pbp_stats_v7, convert_pbp_stats_v5_to_v7, \
        convert_sub_pleague_to_v7, convert_pbp_stats_pleague_to_v7

class FibaGameParser:
    @staticmethod
    def get_game_play_by_play_dataframe_synergy(org_id, game_id, period_id_list):
        #fiba_inbounder.formulas.REG_FULL_GAME_MINS = 48
        
        pbp_json_list = [FibaCommunicator.get_game_play_by_play_synergy(org_id, game_id, p)['data'] for p in period_id_list]
        df = pd.DataFrame(sum(pbp_json_list, []))
        
        #no converting for synergy data
        return df

    @staticmethod
    def get_game_stats_dataframe_synergy(org_id, game_id):
        #TODO get team stats
        
        player_stats_list = [p for p in FibaCommunicator.get_game_player_stats_synergy(org_id, game_id)['data'] if p['participated']]
        player_stats_df = pd.DataFrame(player_stats_list)
        
        #TODO parse player stats
        for p in player_stats_list:
            print p['statistics']['minutes']

        team_id_set = {p['entityId'] for p in player_stats_list}
        starter_dict = {team_id: {p['personId'] for p in player_stats_list if p['starter'] and p['entityId'] == team_id}
                for team_id in team_id_set}

        return player_stats_df, starter_dict

    @staticmethod
    def get_id_tables_synergy(org_id):
        persons_json_list = FibaCommunicator.get_org_persons_synergy(org_id)['data']
        id_table = {p['personId']: p['nameFullLocal'] for p in persons_json_list}

        entities_json_list = FibaCommunicator.get_org_entities_synergy(org_id)['data']
        id_table.update({t['entityId']: t['nameFullLocal'] for t in entities_json_list})

        return id_table

    @staticmethod
    def get_game_stats_dataframe_pleague(game_id):
        fiba_inbounder.formulas.REG_FULL_GAME_MINS = 48
        game_json = FibaCommunicator.get_game_stats_pleague(game_id)
        team_stats_json = list()
        player_stats_list = list()
        team_code_table = dict()
        id_table = dict()

        for ha in ['home', 'away']:
            t = game_json[u'team_stats_' + ha]
            t['Name'] = game_json[ha + '_name']
            t['TeamCode'] = game_json[ha + '_name']
            t['IsHome'] = ha

            t['Periods'] = [
                    {'Id': 'Q' + str(q+1), 'Score': score} if q < 4 else
                    {'Id': 'OT' + str(q-3), 'Score': score}
                    for q, score in enumerate(game_json['score_' + ha + '_p2p'])]
            t['PeriodIdList'] = [p['Id'] for p in t['Periods']]
            
            t['SECS'] = game_json['team_stats_' + ha]['seconds']
            t['TP'] = base60_to(t['SECS'])
       
            team_stats_json.append(t)
            id_table['t' + str(game_json[ha + '_id'])] = t['TeamCode']

            #Player Stats
            for p in game_json['player_stats_' + ha]['total']:
                p['TeamCode'] = t['Name']
                p['JerseyNumber'] = p['jersey']
                p['Name']  = p['name_alt']
                p['NumName'] = u'{num} {name}'.format(num=p['JerseyNumber'].zfill(2), name=p['Name'])
        
                player_stats_list.append(p)
                id_table[p['player_id']] = p['NumName']

        team_a_stats_json = team_stats_json[0]
        team_b_stats_json = team_stats_json[1]
       
        #Oppenent DREB for calculating OREB%
        team_a_stats_json['OPP_DR'] = team_b_stats_json['reb_d']
        team_b_stats_json['OPP_DR'] = team_a_stats_json['reb_d']

        team_a_stats_json['OppTeamCode'] = team_b_stats_json['TeamCode']
        team_b_stats_json['OppTeamCode'] = team_a_stats_json['TeamCode']

        team_stats_df = pd.DataFrame([team_a_stats_json, team_b_stats_json])
        player_stats_df = pd.DataFrame(player_stats_list)
        convert_team_stats_pleague_to_v7(team_stats_df)
        convert_player_stats_pleague_to_v7(player_stats_df)

        return team_stats_df, player_stats_df, 't' + str(game_json['away_id']), 't' + str(game_json['home_id']), id_table

    @staticmethod
    def get_game_sub_dataframe_pleague(game_id, team_id_away, team_id_home):
        fiba_inbounder.formulas.REG_FULL_GAME_MINS = 48
        
        sub_json_list = [
            FibaCommunicator.get_game_sub_pleague(game_id, team_id)
            for team_id in [team_id_away.replace('t', ''), team_id_home.replace('t', '')]]

        df = pd.DataFrame(sum(sub_json_list, [])).sort_values(['createDate'], ascending=[True])
        convert_sub_pleague_to_v7(df, team_id_away)
 
        sub_dict = df.to_dict(orient='records')
        endp_index = [i+1 for i, s in enumerate(sub_dict) if i+1 == len(sub_dict) or s['quarter'] != sub_dict[i+1]['quarter']]

        for i in reversed(endp_index):
            sub_dict.insert(i, {'AC': 'ENDP', 
                'GT': sub_dict[i-1]['GT'] + 1,
                'Time': sub_dict[i-1]['Time'],
                'SA': sub_dict[i-1]['SA'],
                'SB': sub_dict[i-1]['SB'],
                'PTS': 0})
        df = pd.DataFrame(sub_dict)
       
        return df

    @staticmethod
    def get_game_play_by_play_dataframe_pleague(game_id, team_id_away, team_id_home):
        fiba_inbounder.formulas.REG_FULL_GAME_MINS = 48
        
        pbp_json_list = [
            FibaCommunicator.get_game_play_by_play_pleague(game_id, team_id)
            for team_id in [team_id_away.replace('t', ''), team_id_home.replace('t', '')]]

        df = pd.DataFrame(sum(pbp_json_list, []))
        convert_pbp_stats_pleague_to_v7(df, team_id_away, team_id_home)

        return df

    @staticmethod
    def get_game_data_dataframe_v5(match_id):
        fiba_inbounder.formulas.REG_FULL_GAME_MINS = 40
        game_json = FibaCommunicator.get_game_data_v5(match_id)
        team_stats_json = game_json['tm']

        for t in team_stats_json.values():
            #Team Stats
            t['Name'] = t['nameInternational']
            t['TeamCode'] = t['codeInternational']
            t['Periods'] = [{'Id': period.replace('_score', '').replace('p', 'q').upper(), 'Score': score}
                    for period, score in t.iteritems() if period.startswith('p') and period.endswith('_score')]
            if 'ot_score' in t:
                t['Periods'].append({'Id': 'OT', 'Score': t['ot_score']})
            t['PeriodIdList'] = [p['Id'] for p in t['Periods']]

            if base60_from(t['tot_sMinutes']) == 0:
                team_secs = sum([base60_from(p['sMinutes']) for p in t['pl'].values()])
                t['tot_sMinutes'] = base60_to(team_secs)

            #Player Stats
            for p in t['pl'].values():
                p['TeamCode'] = t['codeInternational']
                p['JerseyNumber'] = p['shirtNumber']
                p['Name']  = p['name'].replace(' ', '').upper()
                p['NumName'] = '{num} {name}'.format(num=p['JerseyNumber'].zfill(2), name=p['Name'])

        team_a_stats_json = team_stats_json['1']
        team_b_stats_json = team_stats_json['2']
       
        team_a_player_stats_list = [p for p in team_stats_json['1']['pl'].values()]
        team_b_player_stats_list = [p for p in team_stats_json['2']['pl'].values()]

        #Oppenent DREB for calculating OREB%
        team_a_stats_json['OPP_DR'] = team_b_stats_json['tot_sReboundsDefensive']
        team_b_stats_json['OPP_DR'] = team_a_stats_json['tot_sReboundsDefensive']

        team_a_stats_json['OppTeamCode'] = team_b_stats_json['TeamCode']
        team_b_stats_json['OppTeamCode'] = team_a_stats_json['TeamCode']

        team_stats_df = pd.DataFrame([team_a_stats_json, team_b_stats_json])
        player_stats_df = pd.DataFrame(team_a_player_stats_list + team_b_player_stats_list)
        convert_team_stats_v5_to_v7(team_stats_df)
        convert_player_stats_v5_to_v7(player_stats_df)

        starter_dict = {t['TeamCode']: {p['NumName'] for p in t['pl'].values() if p['starter'] == 1} 
                for t in team_stats_json.values()}

        pbp_df = pd.DataFrame(reversed(game_json['pbp']))
        convert_pbp_stats_v5_to_v7(pbp_df, team_a_stats_json['TeamCode'], team_b_stats_json['TeamCode'])

        shot_df = pd.DataFrame(sum([t['shot'] for t in team_stats_json.values()], [])) 
        convert_pbp_stats_v5_to_v7(shot_df, team_a_stats_json['TeamCode'], team_b_stats_json['TeamCode'])
        convert_xy_v5(shot_df)

        return team_stats_df, player_stats_df, starter_dict, pbp_df, shot_df

    @staticmethod
    def get_game_stats_dataframe_v7(event_id, game_unit):
        fiba_inbounder.formulas.REG_FULL_GAME_MINS = 40
        game_json = FibaCommunicator.get_game_stats_v7(event_id, game_unit)
        team_stats_json = game_json['content']['full']['Competitors']

        for t in team_stats_json:
            #Team Stats
            t['Stats']['Name'] = t['Name']
            t['Stats']['TeamCode'] = t['TeamCode']
            t['Stats']['Periods'] = t['Periods']
            t['Stats']['PeriodIdList'] = [p['Id'] for p in t['Periods']]
            t['Stats']['SECS'] = 60 * 5 * game_time(len(t['Periods']))
            t['Stats']['TP'] = base60_to(t['Stats']['SECS'])
    
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

        team_a_stats_json['OppTeamCode'] = team_b_stats_json['TeamCode']
        team_b_stats_json['OppTeamCode'] = team_a_stats_json['TeamCode']
        
        team_stats_df = pd.DataFrame([team_a_stats_json, team_b_stats_json])
        player_stats_df = pd.DataFrame(team_a_player_stats_list + team_b_player_stats_list)
        convert_secs_v7(player_stats_df)

        return team_stats_df, player_stats_df

    @staticmethod
    def get_game_play_by_play_dataframe_v7(event_id, game_unit, period_id_list):
        fiba_inbounder.formulas.REG_FULL_GAME_MINS = 40
        pbp_json_list = [
            FibaCommunicator.get_game_play_by_play_v7(event_id, game_unit, p)['content']['full']['Items']
            for p in period_id_list]

        df = pd.DataFrame(sum(pbp_json_list, []))
        convert_xy_v7(df)
        convert_pbp_stats_v7(df)
        return df

    @staticmethod
    def get_game_details_dict_v7(event_id, game_unit):
        fiba_inbounder.formulas.REG_FULL_GAME_MINS = 40
        dtl_dict = FibaCommunicator.get_game_details_v7(event_id, game_unit)['content']['full']['Competitors']

        id_table = {k: ((v['TeamCode']) if v['IsTeam'] else ('{num} {short}{sur}'.format(num=v['Bib'].zfill(2), short=v['FirstNameShort'], sur=v['Name'])))
                for k, v in dtl_dict.iteritems()}

        team_id_list = [k for k, v in dtl_dict.iteritems() if v['IsTeam']]
        starter_dict = {t: {v['Id'] for v in dtl_dict.itervalues() if (not v['IsTeam']) and v['Starter'] and v['ParentId']==t} 
                for t in team_id_list}
        
        return id_table, starter_dict
