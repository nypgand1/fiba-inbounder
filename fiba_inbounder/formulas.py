# -*- coding: utf-8 -*-
import numpy as np

def game_time(q):
    if q > 4:
        return 40 + 5 * (q-4)
    return 10 * q

def efg(df):
    return 100 * (((1.5*df['FG3M'] + df['FG2M']) / df['FGA']).replace(np,nan, 0))

def four_factors(df):
    possessions = df['FGA'] + 0.44*df['FTA'] + (df['TO']+df['T_TO']) - (df['OR']+df['T_OR'])
    
    ff = dict()
    ff['PACE'] = 40 * 5 * (possessions / df['TP']).replace(np.nan, 0)
    ff['EFG'] = efg(df)
    ff['TO_RATIO'] = 100 * ((df['TO']+df['T_TO']) / possessions).replace(np.nan, 0)
    ff['OR_PCT'] = 100 * (df['OR'] / (df['OR'] + df['OPP_DR'])).replace(np.nan, 0)
    ff['FT_RATE'] = 100 * (df['FTM'] / df['PTS']).replace(np.nan, 0)

    return ff

def score_bold_md(score):
    if int(score) >= 20:
        return '**{score}**'.format(score=score)
    return str(score)
