# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from fiba_inbounder.settings import LOGGER, REG_FULL_GAME_MINS
from fiba_inbounder.converter import base60_from, base60_to

def time_diff(time_str_before, time_str_after):
    return base60_from(time_str_before) - base60_from(time_str_after)

def score_bold_md(score):
    if int(score) >= (20*REG_FULL_GAME_MINS/40):
        return '**{score}**'.format(score=score)
    return str(score)

def update_team_avg(df):
    for col in ['FG2', 'FG3', 'FT', 'FG']:
        df['{col}P'.format(col=col)] = df.apply(lambda x: 
                (100*float(x['{col}M'.format(col=col)]) / x['{col}A'.format(col=col)]) if x['{col}A'.format(col=col)] > 0
                else 0.0, axis=1)
    
    for col in ['FG2M', 'FG2A', 'FG2P', 'FG3M', 'FG3A', 'FG3P', 'FTM', 'FTA', 'FTP', 
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS',
            'FGM', 'FGA', 'FGP']:
        if col in ['TO', 'PF']:
            df['{col}_RANK'.format(col=col)] = df[col].rank(ascending=True)
        else:
            df['{col}_RANK'.format(col=col)] = df[col].rank(ascending=False)

    for col in ['FG2', 'FG3', 'FT', 'FG']:
        df['{col}P_STR'.format(col=col)] = df['{col}P'.format(col=col)].apply(lambda x: '%.1f%%' % x)
        df['{col}MA_STR'.format(col=col)] = df.apply(lambda x: '%.1f/%.1f' % (
            x['{col}M'.format(col=col)], x['{col}A'.format(col=col)]), axis=1)
        df['{col}MA_RANK'.format(col=col)] = df.apply(lambda x: '%d/%d' % (
            x['{col}M_RANK'.format(col=col)], x['{col}A_RANK'.format(col=col)]), axis=1)

def update_team_key_stats_avg(df):
    for col in ['A_FBP', 'A_SCP', 'A_PAT', 'A_PIP', 'A_PFB']:
        df['{col}_RANK'.format(col=col)] = df[col].rank(ascending=False)

def update_player_avg(df):
    df['TP'] = df['SECS'].apply(lambda x: base60_to(x))
    
    for col in ['FG2', 'FG3', 'FT', 'FG']:
        df['{col}P'.format(col=col)] = df.apply(lambda x: 
                (100*float(x['{col}M'.format(col=col)]) / x['{col}A'.format(col=col)]) if x['{col}A'.format(col=col)] > 0
                else 0.0, axis=1)
    
    for col in ['FG2M', 'FG2A', 'FG2P', 'FG3M', 'FG3A', 'FG3P', 'FTM', 'FTA', 'FTP', 
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS',
            'FGM', 'FGA', 'FGP']:
        if col in ['TO', 'PF']:
            df['{col}_RANK'.format(col=col)] = df[col].rank(ascending=True)
        else:
            df['{col}_RANK'.format(col=col)] = df[col].rank(ascending=False)

    for col in ['FG2', 'FG3', 'FT', 'FG']:
        df['{col}P_STR'.format(col=col)] = df['{col}P'.format(col=col)].apply(lambda x: '%.1f%%' % x)
        df['{col}MA_STR'.format(col=col)] = df.apply(lambda x: '%.1f/%.1f' % (
            x['{col}M'.format(col=col)], x['{col}A'.format(col=col)]), axis=1)
        df['{col}MA_RANK'.format(col=col)] = df.apply(lambda x: '%d/%d' % (
            x['{col}M_RANK'.format(col=col)], x['{col}A_RANK'.format(col=col)]), axis=1)

def update_player_per36(df):
    df['MULTI'] = 36.0 * 60 / df['SECS']
    for col in ['SECS', 'FG2M', 'FG2A', 'FG3M', 'FG3A', 'FTM', 'FTA', 
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS',
            'FGM', 'FGA']:
        df[col] = df[col] * df['MULTI']
    update_player_avg(df)

def update_efg(df):
    df['EFG']= 100 * (((1.5*df['FG3M'] + df['FG2M']) / df['FGA']).replace(np.nan, 0))
    df['EFG_STR'] = df['EFG'].apply(lambda x: '**%.1f%%**' % x if x >= 50 else '%.1f%%' % x)

def update_usg(df):
    df['POSS_WO_OR'] = df['FGA'] + 0.44*df['FTA'] + df['TO']
    df['USG'] = 100 * ((df['POSS_WO_OR'] * (df['SECS'].sum()/5)) / \
            (df['POSS_WO_OR'].sum() * df['SECS'])).replace(np.nan, 0)
    df['USG_STR'] = df['USG'].apply(lambda x: '**%.1f%%**' % x if x >= 25 else '%.1f%%' % x)

def update_poss(df):
    df['POSS'] = df['FGA'] + 0.44*df['FTA'] + df['TO'] - df['OR']
    #OR and then FTA
    df['POSS'] = np.where(df['POSS'] >= 0, df['POSS'], 1)

def update_to_ratio(df):
    update_poss(df)
    df['TO_RATIO'] = 100 * (df['TO'] / df['POSS']).replace(np.nan, 0)
    df['TO_RATIO_STR'] = df['TO_RATIO'].apply(lambda x: '**%.1f%%**' % x if x <= 15 else '%.1f%%' % x)

def update_pace(df):
    update_poss(df)
    df['PACE'] = REG_FULL_GAME_MINS * 60 * 5 * (df['POSS'] / df['SECS']).replace(np.nan, 0)

def update_four_factors(df):
    update_pace(df)
    update_efg(df)
    update_to_ratio(df)

    df['OR_PCT'] = 100 * (df['OR'] / (df['OR'] + df['OPP_DR'])).replace(np.nan, 0)
    df['FT_RATE'] = 100 * (df['FTM'] / df['PTS']).replace(np.nan, 0)

    df['OR_PCT_STR'] = df['OR_PCT'].apply(lambda x: '**%.1f%%**' % x if x >= 30 else '%.1f%%' % x)
    df['FT_RATE_STR'] = df['FT_RATE'].apply(lambda x: '**%.1f%%**' % x if x >= 20 else '%.1f%%' % x)

    for col in ['PACE', 'EFG', 'TO_RATIO', 'OR_PCT', 'FT_RATE']:
        if col == 'TO_RATIO':
            df['{col}_RANK'.format(col=col)] = df[col].rank(ascending=True)
        else:
            df['{col}_RANK'.format(col=col)] = df[col].rank(ascending=False)

def update_rtg(df, team_id):
    update_poss(df)
    df['OFFRTG'] = 100 * np.where(df['T1'].str.match(team_id), (df['PTS'] / df['POSS']).replace(np.nan, 0), 0)
    df['DEFRTG'] = 100 * np.where(~df['T1'].str.match(team_id), (df['PTS'] / df['POSS']).replace(np.nan, 0), 0)

def update_team_rtg(df, opp_df):
    result_list = list()
    for team_id in df['TeamCode'].unique():
        team_opp_df = pd.concat([df[df['TeamCode'].str.match(team_id)], opp_df[opp_df['OppTeamCode'].str.match(team_id)]])
        team_opp_df['T1'] = team_opp_df['TeamCode'].replace(np.nan, '')
        update_rtg(team_opp_df, team_id)
        
        team_opp_df['TeamCode'] = team_id
        team_opp_df = team_opp_df.groupby(['TeamCode'], as_index=False, sort=False).sum()
        result_list.append(team_opp_df[['TeamCode', 'OFFRTG', 'DEFRTG']])
    
    result_df = pd.concat(result_list)
    result_df['NETRTG'] = result_df['OFFRTG'] - result_df['DEFRTG']
    return result_df

def update_zone(df):
    RIM = np.array([(7.5, 1.575)])
    df['DISTANCE'] = np.linalg.norm(df[['X_SIDELINE_M', 'Y_BASELINE_M']].sub(RIM), axis=1)
    df['ZONE'] = np.where(df['AC'] == 'P3',
            np.where(df['Y_BASELINE_M']<=4.725, #3PT
                np.where(df['X_SIDELINE_M']<=7.5, #Corner 3PT
                    9, #Left Corner 3PT
                    13 #Right Corner 3PT
                ),
                np.where(df['X_SIDELINE_M']<5.05, #Non-corner 3PT
                    10, #Left Wing 3PT
                    np.where(df['X_SIDELINE_M']>9.95,
                        12, #Right Wing 3PT
                        11),)), #Center 3PT
            np.where(df['AC'] == 'P2',
                np.where(df['DISTANCE']<=2.25, #2PT
                    0, #Rim 2PT
                    np.where(df['DISTANCE']<=4.5,
                        np.where(df['X_SIDELINE_M']<5.05, #Mid 2PT
                            1, #Left Mid 2PT
                            np.where(df['X_SIDELINE_M']>9.95,
                                3, #Right Mid 2PT
                                2)), #Center Mid 2PT
                        np.where(df['Y_BASELINE_M']<=4.725, #Long 2PT
                            np.where(df['X_SIDELINE_M']<=7.5, #Baseline Long 2PT
                                4, #Left Baseline Long 2PT
                                8), #Right BaselineLong 2PT
                            np.where(df['X_SIDELINE_M']<5.05, #Non-Basebline Long 2PT
                                5, #Left Elbow Long 2PT
                                np.where(df['X_SIDELINE_M']>9.95, 
                                    7, #Right Elbow Long 2PT
                                    6))))), #Center Long 2PT
            None))

def update_zone_pleague(df):
    zone_map = {1: 9, 2: 10, 3: 11, 4: 12, 5: 13,
        6: 4, 7: 5, 8: 6, 9: 7, 10: 8,
        11: 1, 12: 2, 13: 3,
        14: 0, 
        0: 14}
    df['ZONE'] = df.apply(lambda x: zone_map[x['scoringArea']], axis=1)

def update_range(df):
    df['RANGE'] = np.where(df['ZONE']==0, 
            'Rim',
            np.where(df['ZONE']<=3,
                'Mid 2',
                np.where(df['ZONE']<=8,
                    'Long 2',
                    np.where(df['ZONE']<=13,
                        '3PT',
                        None))))

def update_range_stats(df):
    df['FGM/A'] = df.apply(lambda x: '{fgm}/{fga}'.format(fgm=x['FGM'], fga=x['FGA']), axis=1) 
    df['FREQ'] = 100 * (df['FGA'] / df['FGA'].sum()).replace(np.nan, 0)
    df['EFG'] = 100 * (df['FGPTS'] / 2 / df['FGA']).replace(np.nan, 0)
    
    df['FREQ_STR'] = df['FREQ'].apply(lambda x: '**%.1f%%**' % x if x >= 40 else '%.1f%%' % x)
    df['EFG_STR'] = df['EFG'].apply(lambda x: '**%.1f%%**' % x if x >= 50 else '%.1f%%' % x)

def update_lineup(df, starter_dict):
    pbp_dict = df.to_dict(orient='records')

    for i in range(len(pbp_dict)):
        if i == 0:
            for t, s in starter_dict.items():
                pbp_dict[i][t] = s.copy()
                pbp_dict[i]['SECS'] = 0
            continue
        
        for t in starter_dict.keys():
            pbp_dict[i][t] = pbp_dict[i-1][t].copy()
        
        if pbp_dict[i-1]['AC'] == 'SUBST': 
            t = pbp_dict[i-1]['T1']
            if pbp_dict[i-1]['SU'] == '+':
                pbp_dict[i][t].add(pbp_dict[i-1]['C1'])
            elif pbp_dict[i-1]['SU'] == '-':
                if pbp_dict[i-1]['C1'] in pbp_dict[i][t]:
                    pbp_dict[i][t].remove(pbp_dict[i-1]['C1'])
                else:
                    LOGGER.warning(str(pbp_dict[i-1]))
            elif 'C2' in pbp_dict[i-1]:
                LOGGER.warning('%d-%d %s' % (pbp_dict[i-1]['SA'], pbp_dict[i-1]['SB'], pbp_dict[i-1]['Time']))
                LOGGER.warning(pbp_dict[i][t])
               
                pbp_dict[i][t].add(pbp_dict[i-1]['C1'])
                LOGGER.warning(pbp_dict[i][t])
               
                pbp_dict[i][t].remove(pbp_dict[i-1]['C2'])
                LOGGER.warning(pbp_dict[i][t])

        if pbp_dict[i-1]['AC'] == 'ENDP' or pbp_dict[i-1] == 'ENDG':
            pbp_dict[i]['SECS'] = 0
        elif pbp_dict[i]['Time'] is np.nan:
            pass
        else:
            pre_time_p = [p for p in pbp_dict[:i] if p['Time'] is not np.nan][-1]
            pbp_dict[i]['SECS'] = time_diff(pre_time_p['Time'], pbp_dict[i]['Time'])

    pbp_df = pd.DataFrame(pbp_dict)
    def to_sorted_tuple(x):
        result = list(x)
        result.sort()
        return tuple(result)
    for t in starter_dict.keys():
        df[t] = pbp_df[t].apply(lambda x: to_sorted_tuple(x))
    df['SECS'] = pbp_df['SECS']

def update_lineup_synergy(df, starter_dict, id_table):
    for t in starter_dict.keys():
        df.loc[:, t] = [starter_dict[t]] * len(df)
  
        df['in_{team}'.format(team=t)] = df.apply(lambda x: [x['personId']] if (x['eventType']=='substitution') and (x['subType']=='in') and (x['entityId']==t) else [], axis=1)
        df['out_{team}'.format(team=t)] = df.apply(lambda x: [x['personId']] if (x['eventType']=='substitution') and (x['subType']=='out') and (x['entityId']==t) else [], axis=1)
        in_cum_team = 'in_cum_{team}'.format(team=t)
        out_cum_team = 'out_cum_{team}'.format(team=t)
        df[in_cum_team] = df['in_{team}'.format(team=t)].cumsum()
        df[out_cum_team] = df['out_{team}'.format(team=t)].cumsum()
       

        print '\n[team %s]' % t
        for i, r in df[(df['eventType']=='substitution') & (df['entityId']==t) & (df['periodId']==1)].iterrows():
                print r['eventId'], r['periodId'], r['clock'], r['eventType'], r['subType'], id_table.get(r['personId'], r['personId']), r['timestamp']

        print '----'
        def cum_add_remove(r):
            #TODO print for debug
            if r['eventType'] == 'substitution' and r['entityId']==t:
                print r['eventId'], r['periodId'], r['clock'], r['eventType'], r['subType'], id_table.get(r['personId'], r['personId']), r['timestamp']
            lineup = list(r[t])
            for p in r[in_cum_team]:
                lineup.append(p)
            for p in r[out_cum_team]:
                lineup.remove(p)
            #TODO print for debug
            if r['eventType'] == 'substitution' and r['entityId']==t:
                print 'after sub'
                for p in [id_table.get(p, p) for p in lineup]:
                    print p
            return set(lineup)

        df[t] = df.apply(lambda x: cum_add_remove(x), axis=1)

        def set_period_event_clock(r):
            if r['eventType'] != 'period':
                return r['clock']
            else:
                if r['subType'] in ['pending', 'start']:
                    if r['periodId'] in [1, 2, 3, 4]:
                        return 'PT12M0S'
                    else: #overtime
                        return 'PT5M0S'
                elif r['subType'] in ['end', 'confirmed']:
                        return 'PT0M0S'
                else:
                    return r['clock']
        df['clock'] = df.apply(lambda x: set_period_event_clock(x), axis=1)

def get_sub_map_synergy(df): 
    result_list = list()
    for t in [t for t in df['entityId'].unique() if not pd.isna(t)]:
        df_team = df[(df['entityId']==t) | ((df['eventType']=='period') & (df['subType'].isin(['pending', 'confirmed'])))]
        for p in [p for p in df_team['personId'].unique() if not pd.isna(p)]:
            df_team['selected'] = df_team.apply(lambda x: (x['personId']==p) or ((x['eventType']=='period') and (p in x[t])), axis=1)
            df_player = df_team[df_team['selected']].reindex()
            
            df_player['clock'] = pd.to_datetime(df_player['clock'], format='PT%MM%SS')
            df_player['clock_prev'] = df_player['clock'].shift(1)
            df_duration = df_player[df_player['subType'].isin(['out', 'confirmed'])]

            player_sub_map = {'entityId': t, 'personId': p, 'fixtureId': [f for f in df['fixtureId'] if not pd.isin(f)][0]}
            for i, r in df_duration.iterrows():
                #TODO: if it's not 12-min period
                if r['periodId'] not in [1, 2, 3, 4]: #overtime
                    player_sub_map['OT'] = player_sub_map.get('OT', 0) + (r['clock_prev']-r['clock']).seconds
                elif r['clock'].minute == r['clock_prev'].minute:
                    if r['clock'].second != r['clock_prev'].second: #not same
                        pm_str = '{period}Q{minute:0>2d}M'.format(period=r['periodId'], minute=11-r['clock'].minute)
                        player_sub_map[pm_str] = player_sub_map.get(pm_str, 0) + r['clock_prev'].second - r['clock'].second
                else:
                    if r['clock_prev'].second: #not 0 Seconds
                        pm_str = '{period}Q{minute:0>2d}M'.format(period=r['periodId'], minute=11-r['clock_prev'].minute)
                        player_sub_map[pm_str] = player_sub_map.get(pm_str, 0) + r['clock_prev'].second
                    pm_str = '{period}Q{minute:0>2d}M'.format(period=r['periodId'], minute=11-r['clock'].minute)
                    player_sub_map[pm_str] = player_sub_map.get(pm_str, 0) + 60 - r['clock'].second
                    for m in range(r['clock_prev'].minute-1, r['clock'].minute, -1):
                        pm_str = '{period}Q{minute:0>2d}M'.format(period=r['periodId'], minute=11-m)
                        player_sub_map[pm_str] = 60
            result_list.append(player_sub_map)
        
    result_df = pd.DataFrame(result_list)
    return result_df

def get_score_map_synergy(df): 
    result_list = list()
    point_map = {'freeThrow': 1, '2pt': 2, '3pt': 3}
    
    for t in [t for t in df['entityId'].unique() if not pd.isna(t)]:
        df_team = df[(df['entityId']==t) & (df['success'])]
        df_team['score_point'] = df_team['eventType'].apply(lambda x: point_map[x])
        df_team['clock'] = pd.to_datetime(df_team['clock'], format='PT%MM%SS')
        
        team_score_map = {'{period}Q{minute:0>2d}M'.format(period=p, minute=m): 0 for p in [1, 2, 3, 4] for m in range(0, 12)}
        team_score_map['entityId'] = t
        team_score_map['fixtureId'] = [f for f in df['fixtureId'] if not pd.isna(f)][0]
        
        for i, r in df_team.iterrows():
            if r['periodId'] not in [1, 2, 3, 4]: #overtime
                team_score_map['OT'] = team_score_map.get('OT', 0) + r['score_point']
            else:
                pm_str = '{period}Q{minute:0>2d}M'.format(period=r['periodId'], minute=11-r['clock'].minute)
                team_score_map[pm_str] = team_score_map[pm_str] + r['score_point']
        result_list.append(team_score_map)

    result_df = pd.DataFrame(result_list)
    return result_df

def get_lineup_stats(df, team_id, id_table=None):
    update_efg(df)
    update_to_ratio(df)
    update_rtg(df, team_id)

    df['EFG'] = np.where(df['T1'].str.match(team_id), df['EFG'], 0)
    df['TO_RATIO'] = np.where(df['T1'].str.match(team_id), df['TO_RATIO'], 0)
    df['PM'] = np.where(df['T1'].str.match(team_id), df['PTS'], -df['PTS'])
    df['A/T'] = np.where(df['T1'].str.match(team_id), (df['AS'] / df['TO']), 0)
  
    result_df = df.groupby([team_id], as_index=False, sort=False).sum()
    result_df = result_df[(result_df['SECS']>0) | (~(result_df['POSS']==0))]

    update_pace(result_df)
    result_df['PACE'] = result_df['PACE'] / 10
    result_df['TP'] = result_df['SECS'].apply(lambda x: base60_to(x))
    
    def lineup_name(team_lineup, secs, offrtg, defrtg, pm):
        name_list = [id_table[p] if p in id_table else p for p in team_lineup]
        name_list.sort()
        name_str = ', '.join(name_list)
        if ((secs>2*60) and (offrtg>=100) and (defrtg <100)) or (pm>=10):
            return '**%s**' % name_str
        else:    
            return name_str

    result_df['LINEUP_NAME'] = result_df.apply(lambda x: lineup_name(x[team_id], x['SECS'], x['OFFRTG'], x['DEFRTG'], x['PM']), axis=1)

    result_df['EFG_STR'] = result_df['EFG'].apply(lambda x: '**%.1f%%**' % x if x >= 50 else '%.1f%%' % x)
    result_df['TO_RATIO_STR'] = result_df['TO_RATIO'].apply(lambda x: '**%.1f%%**' % x if x <= 15 else '%.1f%%' % x)
    result_df['A/T_STR'] = result_df['A/T'].apply(lambda x: '**%.2f**' % x if x >= 1.5 else '%.2f' % x)
    result_df['NETRTG'] = result_df['OFFRTG'] - result_df['DEFRTG']

    return result_df[[team_id, 'LINEUP_NAME', 'SECS', 'TP', 'PACE', 'PM', 'EFG', 'EFG_STR', 'TO_RATIO_STR', 'A/T_STR', 'OFFRTG', 'DEFRTG', 'NETRTG']]

def get_on_off_stats(df, team_id, id_table=None):
    update_rtg(df, team_id)
    on_off_df = df.groupby(['PLAYER', 'ON'], as_index=False, sort=False).sum()
    on_off_df['PLAYER_NAME'] = on_off_df['PLAYER'].apply(lambda x: id_table[x] if x in id_table else x)
    
    on_off_df['OFFRTG_OFF'] = on_off_df.apply(lambda x: 0 if x['ON'] else x['OFFRTG'], axis=1)
    on_off_df['DEFRTG_OFF'] = on_off_df.apply(lambda x: 0 if x['ON'] else x['DEFRTG'], axis=1)
    on_off_df['SECS_OFF'] = on_off_df.apply(lambda x: 0 if x['ON'] else x['SECS'], axis=1)
    on_off_df['OFFRTG'] = on_off_df.apply(lambda x: x['OFFRTG'] if x['ON'] else 0, axis=1)
    on_off_df['DEFRTG'] = on_off_df.apply(lambda x: x['DEFRTG'] if x['ON'] else 0, axis=1)
    on_off_df['SECS'] = on_off_df.apply(lambda x: x['SECS'] if x['ON'] else 0, axis=1)

    on_off_df['NETRTG'] = on_off_df['OFFRTG'] - on_off_df['DEFRTG']
    on_off_df['NETRTG_OFF'] = on_off_df['OFFRTG_OFF'] - on_off_df['DEFRTG_OFF']

    result_df = on_off_df.groupby(['PLAYER_NAME'], as_index=False, sort=False).sum()
    result_df['OFFRTG_DIFF'] = result_df['OFFRTG'] - result_df['OFFRTG_OFF']
    result_df['DEFRTG_DIFF'] = result_df['DEFRTG'] - result_df['DEFRTG_OFF']
    result_df['NETRTG_DIFF'] = result_df['NETRTG'] - result_df['NETRTG_OFF']

    result_df['OFFRTG_DIFF_STR'] = result_df['OFFRTG_DIFF'].apply(lambda x: '**%.1f**' % x if x>0 else '%.1f' % x)
    result_df['DEFRTG_DIFF_STR'] = result_df['DEFRTG_DIFF'].apply(lambda x: '**%.1f**' % x if x<0 else '%.1f' % x)

    result_df['TP'] = result_df['SECS'].apply(lambda x: base60_to(x))
    result_df['TP_OFF'] = result_df['SECS_OFF'].apply(lambda x: base60_to(x))

    return result_df[['PLAYER_NAME', 'SECS', 'SECS_OFF', 'TP', 'TP_OFF', 'OFFRTG', 'DEFRTG', 'NETRTG', 'OFFRTG_OFF', 'DEFRTG_OFF', 'NETRTG_OFF', 
        'OFFRTG_DIFF', 'DEFRTG_DIFF', 'NETRTG_DIFF', 'OFFRTG_DIFF_STR', 'DEFRTG_DIFF_STR']]

def get_player_mins_plus_minus(df, team_id_away):
    df['SA_DIFF'] = df.apply(lambda x: -x['SA'] if x['SU']=='+' else x['SA'], axis=1)
    df['SB_DIFF'] = df.apply(lambda x: -x['SB'] if x['SU']=='+' else x['SB'], axis=1)
   
    df['SECS'] = df['Time'].apply(lambda x: base60_from(x))
    df['SECS_DIFF'] = df.apply(lambda x: x['SECS'] if x['SU']=='+' else -x['SECS'], axis=1)

    result_df = df.groupby(['T1', 'C1'], as_index=False, sort=False).sum()
    result_df['TP'] = result_df['SECS_DIFF'].apply(lambda x: base60_to(x))
    result_df['PM'] = np.where(result_df['T1']==team_id_away, result_df['SA_DIFF']-result_df['SB_DIFF'], 
            result_df['SB_DIFF']-result_df['SA_DIFF'])
    
    return result_df[['T1', 'C1', 'TP', 'PM']]
