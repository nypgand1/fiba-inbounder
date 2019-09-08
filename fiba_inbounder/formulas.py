# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

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
    while secs >= 60:
        d = secs / 60
        num_list.append('%02d' % (secs - 60*d))
        secs = d
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

def update_secs_v7(df):
    df['SECS'] = df['TP'].replace(np.nan, '00:00').apply(lambda x: base60_from(x))

def update_xy_v7(df):
    #Left Corner as (0, 0) in Meters
    df['X_SIDELINE_M'] = df['SX'].apply(lambda x: float(x)/280*15)
    df['Y_BASELINE_M'] = df['SY'].apply(lambda y: float(y)/280*14)

def update_stats_v7(df):
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
            np.nan))

def update_range(df):
    df['RANGE'] = np.where(df['ZONE']==0, 
            'Rim',
            np.where(df['ZONE']<=3,
                'Mid 2',
                np.where(df['ZONE']<=8,
                    'Long 2',
                    np.where(df['ZONE']<=13,
                        '3PT',
                        np.nan))))

def update_range_stats(df):
    df['FGM/A'] = df['FGM'].map('{:,.0f}'.format) + '/' + df['FGA'].map('{:,.0f}'.format)
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
                pbp_dict[i][t].remove(pbp_dict[i-1]['C1'])

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

    df['EFG'] = np.where(df['T1'].str.match(team_id), df['EFG'], 0)
    df['TO_RATIO'] = np.where(df['T1'].str.match(team_id), df['TO_RATIO'], 0)
    df['PM'] = np.where(df['T1'].str.match(team_id), df['PTS'], -df['PTS'])
    df['OFFRTG'] = 100 * np.where(df['T1'].str.match(team_id), (df['PTS'] / df['POSS']).replace(np.nan, 0), 0)
    df['DEFRTG'] = 100 * np.where(~df['T1'].str.match(team_id), (df['PTS'] / df['POSS']).replace(np.nan, 0), 0)
    df['A/T'] = np.where(df['T1'].str.match(team_id), (df['AS'] / df['TO']), 0)
   
    result_df = df.groupby([team_id], as_index=False, sort=False).sum()
    result_df = result_df[(result_df['SECS']>0) | (~(result_df['POSS']==0))]

    update_pace(result_df)
    result_df['PACE'] = result_df['PACE'] / 10
    result_df['TP'] = result_df['SECS'].apply(lambda x: base60_to(x))
    
    def lineup_name(team_lineup, secs, offrtg, defrtg, pm):
        name_str = str([id_table[p] if p in id_table else p for p in team_lineup])
        name_str = name_str.replace("[u'", "").replace("', u'", ", ").replace("']", "")
        if ((secs>2*60) and (offrtg>=100) and (defrtg <100)) or (pm>=10):
            return '**%s**' % name_str
        else:    
            return name_str
    result_df['LINEUP_NAME'] = result_df.apply(lambda x: lineup_name(x[team_id], x['SECS'], x['OFFRTG'], x['DEFRTG'], x['PM']), axis=1)

    result_df['EFG_STR'] = result_df['EFG'].apply(lambda x: '**%.1f%%**' % x if x >= 50 else '%.1f%%' % x)
    result_df['TO_RATIO_STR'] = result_df['TO_RATIO'].apply(lambda x: '**%.1f%%**' % x if x <= 15 else '%.1f%%' % x)
    result_df['A/T_STR'] = result_df['A/T'].apply(lambda x: '**%.2f**' % x if x >= 1.5 else '%.2f' % x)
    result_df['NETRTG'] = result_df['OFFRTG'] - result_df['DEFRTG']

    return result_df[[team_id, 'LINEUP_NAME', 'TP', 'PACE', 'PM', 'EFG', 'EFG_STR', 'TO_RATIO_STR', 'A/T_STR', 'OFFRTG', 'DEFRTG', 'NETRTG']]
