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

def score_bold_md(score):
    if int(score) >= 20:
        return '**{score}**'.format(score=score)
    return str(score)
