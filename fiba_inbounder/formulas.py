# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from settings import LOGGER

def game_time(q):
    if q > 4:
        return 40 + 5 * (q-4)
    return 10 * q

def base60_from(time_str):
    num_list = time_str.split(':')
    secs = 0
    for i in num_list:
        secs = secs * 60 + int(i)
    return secs

def base60_to(secs):
    secs = int(secs)
    num_list = list()
    if secs >= 60:
        d = secs / 60
        num_list.append('%02d' % (secs - 60*d))
        num_list.append('%02d' % d)
    else:
        num_list.append('%02d' % secs)

    if len(num_list) == 1:
       num_list.append('00')
    num_list.reverse()

    return ':'.join(num_list)

def time_diff(time_str_before, time_str_after):
    return base60_from(time_str_before) - base60_from(time_str_after)

def score_bold_md(score):
    if int(score) >= 20:
        return '**{score}**'.format(score=score)
    return str(score)

def update_team_stats_v5_to_v7(df):
    df['AS'] = df['tot_sAssists']
    df['BS'] = df['tot_sBlocks']
    df['FGA'] = df['tot_sFieldGoalsAttempted']
    df['FGM'] = df['tot_sFieldGoalsMade']
    df['PF'] = df['tot_sFoulsTotal']
    df['FTA'] = df['tot_sFreeThrowsAttempted']
    df['FTM'] = df['tot_sFreeThrowsMade']
    df['TP'] = df['tot_sMinutes'].replace(np.nan, '00:00')
    df['SECS'] = df['tot_sMinutes'].replace(np.nan, '00:00').apply(lambda x: base60_from(x))
    df['PTS'] = df['tot_sPoints']
    df['DR']  = df['tot_sReboundsDefensive']
    df['OR'] = df['tot_sReboundsOffensive']
    df['REB'] = df['tot_sReboundsTotal']
    df['ST'] = df['tot_sSteals']
    df['FG3A'] = df['tot_sThreePointersAttempted']
    df['FG3M'] = df['tot_sThreePointersMade']
    df['TO'] = df['tot_sTurnovers']
    df['FG2A'] = df['tot_sTwoPointersAttempted']
    df['FG2M'] = df['tot_sTwoPointersMade']

    df['A_FBP'] = df['tot_sPointsFastBreak']
    df['A_SCP'] = df['tot_sPointsSecondChance']
    df['A_PAT'] = df['tot_sPointsFromTurnovers']
    df['A_PIP'] = df['tot_sPointsInThePaint']
    df['A_PFB'] = df['tot_sBenchPoints']

def update_player_stats_v5_to_v7(df):
    df['AS'] = df['sAssists']
    df['BS'] = df['sBlocks']
    df['FGA'] = df['sFieldGoalsAttempted']
    df['FGM'] = df['sFieldGoalsMade']
    df['PF'] = df['sFoulsPersonal']
    df['FTA'] = df['sFreeThrowsAttempted']
    df['FTM'] = df['sFreeThrowsMade']
    df['FTP'] = df['sFreeThrowsPercentage']
    df['TP'] = df['sMinutes'].replace(np.nan, '00:00')
    df['SECS'] = df['sMinutes'].replace(np.nan, '00:00').apply(lambda x: base60_from(x))
    df['PTS'] = df['sPoints']
    df['DR']  = df['sReboundsDefensive']
    df['OR'] = df['sReboundsOffensive']
    df['REB'] = df['sReboundsTotal']
    df['ST'] = df['sSteals']
    df['FG3A'] = df['sThreePointersAttempted']
    df['FG3M'] = df['sThreePointersMade']
    df['TO'] = df['sTurnovers']
    df['FG2A'] = df['sTwoPointersAttempted']
    df['FG2M'] = df['sTwoPointersMade']
    df['PM'] = df['sPlusMinusPoints']

    df['JerseyNumber'] = df['shirtNumber']
    df['Name'] = df['name'].str.replace(' ', '').str.upper()

def update_team_avg(df):
    for col in ['FG2', 'FG3', 'FT', 'FG']:
        df['{col}P'.format(col=col)] = df.apply(lambda x: 
                (100*float(x['{col}M'.format(col=col)]) / x['{col}A'.format(col=col)]) if x['{col}A'.format(col=col)] > 0
                else 0.0, axis=1)
    
    for col in ['FG2M', 'FG2A', 'FG2P', 'FG3M', 'FG3A', 'FG3P', 'FTM', 'FTA', 'FTP', 
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS',
            'FGM', 'FGA', 'FGP',
            'A_FBP', 'A_SCP', 'A_PAT', 'A_PIP', 'A_PFB']:
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
    df['PACE'] = 40 * 60 * 5 * (df['POSS'] / df['SECS']).replace(np.nan, 0)

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

def update_secs_v7(df):
    df['SECS'] = df['TP'].replace(np.nan, '00:00').apply(lambda x: base60_from(x))

def update_xy_v7(df):
    #Left Corner as (0, 0) in Meters
    df['X_SIDELINE_M'] = df['SX'].apply(lambda x: float(x)/280*15)
    df['Y_BASELINE_M'] = df['SY'].apply(lambda y: float(y)/280*14)

def update_xy_v5(df):
    #Left Corner as (0, 0) in Meters
    df['X_SIDELINE_M'] = df.apply(lambda s: float(s['y'])/100*15 if s['x']<=50 else float(100-s['y'])/100*15, axis=1)
    df['Y_BASELINE_M'] = df.apply(lambda s: float(s['x'])/50*14 if s['x']<=50 else float(100-s['x'])/50*14, axis=1)

def update_pbp_stats_v7(df):
    #TODO: Still Lots of Stats
    df['FG2M'] = np.where((df['AC']=='P2') & (df['SU']=='+'), 1, 0)
    df['FG2A'] = np.where(df['AC']=='P2', 1, 0)
    df['FG3M'] = np.where((df['AC']=='P3') & (df['SU']=='+'), 1, 0)
    df['FG3A'] = np.where(df['AC']=='P3', 1, 0)

    df['FGA'] = df['FG2A'] + df['FG3A']
    df['FGM'] = df['FG2M'] + df['FG3M']
    df['FGPTS'] = 2 * df['FG2M'] + 3 *df['FG3M']
   
    df['FTM'] = np.where((df['AC']=='FT') & (df['SU']=='+'), 1, 0)
    df['FTA'] = np.where(df['AC']=='FT', 1, 0)
    df['PTS'] = df['FGPTS'] + df['FTM']
    
    df['OR'] = np.where((df['AC'].str.contains('REB')) & (df['Z1']=='O'), 1, 0)
    df['DR'] = np.where((df['AC'].str.contains('REB')) & (df['Z1']=='D'), 1, 0)
    df['REB'] = df['OR'] + df['DR']

    df['AS'] = np.where(df['AC']=='ASS', 1, 0)
    df['TO'] = np.where(df['AC']=='TO', 1, 0)

def update_pbp_stats_v5_to_v7(df, ta_code, tb_code):
    #TODO: Still Lots of Stats
    df['T1'] = np.where(df['tno']==1, ta_code,
            np.where(df['tno']==2, tb_code, None))
    df['OppTeamCode'] = np.where(df['tno']==1, tb_code,
            np.where(df['tno']==2, ta_code, None))
    df['C1'] = df.apply(lambda x: '{num} {name}'.format(
        num=x['shirtNumber'].zfill(2), name=x['player'].replace(' ', '').upper()), axis=1)
    df['AC'] = np.where((df['actionType']=='period') & (df['subType']=='end'), 'ENDP',
            np.where(df['actionType']=='substitution', 'SUBST', 
            np.where(df['actionType']=='2pt', 'P2',
            np.where(df['actionType']=='3pt', 'P3', None))))
    df['SU'] = np.where(df['actionType']=='substitution',
                np.where(df['subType']=='in', '+', 
                np.where(df['subType']=='out', '-', None)),
            None)
    if 'gt' in df:
        df['Time'] = df['gt']

    if 'success' in df:
        df['FG2M'] = np.where((df['actionType']=='2pt') & (df['success']==1), 1, 0)
        df['FG3M'] = np.where((df['actionType']=='3pt') & (df['success']==1), 1, 0)
    elif 'r' in df:
        df['FG2M'] = np.where((df['actionType']=='2pt') & (df['r']==1), 1, 0)
        df['FG3M'] = np.where((df['actionType']=='3pt') & (df['r']==1), 1, 0)
    else:
        df['FG2M'] = 0
        df['FG3M'] = 0
    df['FG2A'] = np.where(df['actionType']=='2pt', 1, 0)
    df['FG3A'] = np.where(df['actionType']=='3pt', 1, 0)

    df['FGA'] = df['FG2A'] + df['FG3A']
    df['FGM'] = df['FG2M'] + df['FG3M']
    df['FGPTS'] = 2 * df['FG2M'] + 3 *df['FG3M']
   
    if 'success' in df:
        df['FTM'] = np.where((df['actionType']=='freethrow') & (df['success']==1), 1, 0)
    else:
        df['FTM'] = 0
    df['FTA'] = np.where(df['actionType']=='freethrow', 1, 0)
    df['PTS'] = df['FGPTS'] + df['FTM']
    
    df['OR'] = np.where((df['actionType']=='rebound') & (df['subType']=='offensive'), 1, 0)
    df['DR'] = np.where((df['actionType']=='rebound') & (df['subType']=='defensive'), 1, 0)
    df['REB'] = df['OR'] + df['DR']

    df['AS'] = np.where(df['actionType']=='assist', 1, 0)
    df['TO'] = np.where(df['actionType']=='turnover', 1, 0)
    
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
            for t, s in starter_dict.iteritems():
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

        if pbp_dict[i-1]['AC'] == 'ENDP':
            pbp_dict[i]['SECS'] = 0
        else:
            pbp_dict[i]['SECS'] = time_diff(pbp_dict[i-1]['Time'], pbp_dict[i]['Time'])

    pbp_df = pd.DataFrame(pbp_dict)
    def to_sorted_tuple(x):
        result = list(x)
        result.sort()
        return tuple(result)
    for t in starter_dict.keys():
        df[t] = pbp_df[t].apply(lambda x: to_sorted_tuple(x))
    df['SECS'] = pbp_df['SECS']

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
        name_str = str(name_list)
        name_str = name_str.replace("['", "").replace("', '", ", ").replace("']", "")
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
    on_off_df['DEFRTG'] = on_off_df.apply(lambda x: x['DEFRTG'] if x['ON'] else 0,axis=1)
    on_off_df['SECS'] = on_off_df.apply(lambda x: x['SECS'] if x['ON'] else 0,axis=1)

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
