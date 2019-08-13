# -*- coding: utf-8 -*-
import numpy as np

def game_time(q):
    if q > 4:
        return 40 + 5 * (q-4)
    return 10 * q

def update_efg(df):
    df['EFG']= 100 * (((1.5*df['FG3M'] + df['FG2M']) / df['FGA']).replace(np.nan, 0))
    df['EFG_STR'] = df['EFG'].apply(lambda x: '**%.1f%%**' % x if x >= 50 else '%.1f%%' % x)

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

def update_xy_v7(df):
    #Left Corner as (0, 0) in Meters
    df['X_SIDELINE_M'] = df['SX']/280*15
    df['Y_BASELINE_M'] = df['SY']/280*14

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

def score_bold_md(score):
    if int(score) >= 20:
        return '**{score}**'.format(score=score)
    return str(score) 
