# -*- coding: utf-8 -*-
import numpy as np

def game_time(q):
    if q > 4:
        return 40 + 5 * (q-4)
    return 10 * q

def update_efg(df):
    df['EFG']= 100 * (((1.5*df['FG3M'] + df['FG2M']) / df['FGA']).replace(np.nan, 0))
    df['EFG_STR'] = df['EFG'].apply(lambda x: '**%.1f%%**' % x if x >= 50 else '%.1f%%' % x)

def update_usg(df):
    df['POSS_WO_OR'] = df['FGA'] + 0.44*df['FTA'] + df['TO']
    df['USG'] = 100 * ((df['POSS_WO_OR'] * (df['SECS'].sum()/5)) / \
            (df['POSS_WO_OR'].sum() * df['SECS'])).replace(np.nan, 0)
    df['USG_STR'] = df['USG'].apply(lambda x: '**%.1f%%**' % x if x >= 25 else '%.1f%%' % x)

def update_four_factors(df):
    df['POSS'] = df['FGA'] + 0.44*df['FTA'] + df['TO'] - df['OR']
   
    update_efg(df)
    df['PACE'] = 40 * 5 * (df['POSS'] / df['TP']).replace(np.nan, 0)
    df['TO_RATIO'] = 100 * (df['TO'] / df['POSS']).replace(np.nan, 0)
    df['OR_PCT'] = 100 * (df['OR'] / (df['OR'] + df['OPP_DR'])).replace(np.nan, 0)
    df['FT_RATE'] = 100 * (df['FTM'] / df['PTS']).replace(np.nan, 0)

    df['TO_RATIO_STR'] = df['TO_RATIO'].apply(lambda x: '**%.1f%%**' % x if x <= 15 else '%.1f%%' % x)
    df['OR_PCT_STR'] = df['OR_PCT'].apply(lambda x: '**%.1f%%**' % x if x >= 30 else '%.1f%%' % x)
    df['FT_RATE_STR'] = df['FT_RATE'].apply(lambda x: '**%.1f%%**' % x if x >= 20 else '%.1f%%' % x)

def update_secs_v7(df):
    def base60(num_list):
        result = 0
        for i in num_list:
            result = result * 60 + int(i)
        return result

    df['SECS'] = df['TP'].apply(lambda x: base60(x.split(':')))

def update_xy_v7(df):
    #Left Corner as (0, 0) in Meters
    df['X_SIDELINE_M'] = df['SX'].apply(lambda x: float(x)/280*15)
    df['Y_BASELINE_M'] = df['SY'].apply(lambda y: float(y)/280*14)

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
    
    df['FGA'] = np.where((df['AC']=='P3'), 1, 
            np.where(df['AC']=='P2', 1, np.nan))
    df['FGM'] = np.where((df['AC']=='P3'), 
            np.where(df['SU']=='+', 1, 0), 
            np.where(df['AC'] == 'P2', 
                np.where(df['SU']=='+', 1, 0), 
                np.nan))
    df['PTS'] = np.where((df['AC']=='P3'), 
            np.where(df['SU']=='+', 3, 0), 
            np.where(df['AC'] == 'P2', 
                np.where(df['SU']=='+', 2, 0), 
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
    df['EFG'] = 100 * (df['PTS'] / 2 / df['FGA']).replace(np.nan, 0)
    
    df['FREQ_STR'] = df['FREQ'].apply(lambda x: '**%.1f%%**' % x if x >= 40 else '%.1f%%' % x)
    df['EFG_STR'] = df['EFG'].apply(lambda x: '**%.1f%%**' % x if x >= 50 else '%.1f%%' % x)

def score_bold_md(score):
    if int(score) >= 20:
        return '**{score}**'.format(score=score)
    return str(score) 
