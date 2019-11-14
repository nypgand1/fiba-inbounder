import numpy as np
import pandas as pd

from fiba_inbounder.formulas import update_xy_v7, update_pbp_stats_v7, update_zone, update_range, update_lineup
from actions_sample import sample

ac_df = pd.DataFrame([
    {'AC': 'P2', 'SX': '140', 'SY': '31.5', 'SU': '-'}, #Rim 
    {'AC': 'P2', 'SX': '148.0', 'SY': '36', 'SU': '+'}, #Rim
        
    {'AC': 'P3', 'SX': '238.0', 'SY': '130', 'SU': '-'}, #Right Wing 3PT
    {'AC': 'P3', 'SX': '156.0', 'SY': '167', 'SU': '+'}, #Top 3PT
    {'AC': 'P3', 'SX': '5.0', 'SY': '52'}, #Left Corner 3PT
    {'AC': 'P3', 'SX': '263', 'SY': '93'}, #Right Corner 3PT
    {'AC': 'P3', 'SX': '56', 'SY': '146'}, #Left Wing 3PT

    {'AC': 'P2', 'SX': '151', 'SY': '104'}, #Center Mid 2PT
    {'AC': 'P2', 'SX': '78', 'SY': '57'}, #Left Mid 2PT
    {'AC': 'P2', 'SX': '201', 'SY': '41'}, #Right Mid 2PT

    {'AC': 'P2', 'SX': '50', 'SY': '36'}, #Left Baseline Long 2PT
    {'AC': 'P2', 'SX': '226', 'SY': '73'}, #Right Baseline Long 2PT
    {'AC': 'P2', 'SX': '198', 'SY': '109'}, #Right Elbow Long 2PT
    {'AC': 'P2', 'SX': '148', 'SY': '125'}, #Center Long 2PT
    {'AC': 'P2', 'SX': '81', 'SY': '104'}, #Left Elbow Long 2PT
    
    {'AC': 'REB', 'Z1': 'O'}, #OREB
    {'AC': 'TREB', 'Z1': 'D'}, #DREB
])

sample_df = pd.DataFrame(sample)
starter_dict = {
    'T_65245': {'P_205482', 'P_224350', 'P_206446', 'P_194018', 'P_199054'},
    'T_57840': {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
}

def test_update_xy_v7():
    update_xy_v7(ac_df)
    ac_dict = ac_df.to_dict(orient='records')
    assert ac_dict[0]['X_SIDELINE_M'] == 7.5
    assert ac_dict[0]['Y_BASELINE_M'] == 1.575

def test_update_pbp_stats_v7():
    update_pbp_stats_v7(ac_df)
    ac_dict = ac_df.to_dict(orient='records')
    assert ac_dict[15]['OR'] == 1
    assert ac_dict[16]['DR'] == 1

def test_update_zone():
    update_zone(ac_df)
    ac_dict = ac_df.to_dict(orient='records')
    
    assert ac_dict[0]['DISTANCE'] == 0
    assert ac_dict[1]['DISTANCE'] == 0.48404387134613663
    assert ac_dict[2]['DISTANCE'] == 7.198480742490043
    assert ac_dict[3]['DISTANCE'] == 6.829005701970896
    
    assert ac_dict[0]['ZONE'] == 0
    assert ac_dict[1]['ZONE'] == 0
    
    assert ac_dict[2]['ZONE'] == 12
    assert ac_dict[3]['ZONE'] == 11
    assert ac_dict[4]['ZONE'] == 9
    assert ac_dict[5]['ZONE'] == 13
    assert ac_dict[6]['ZONE'] == 10
    
    assert ac_dict[7]['ZONE'] == 2
    assert ac_dict[8]['ZONE'] == 1
    assert ac_dict[9]['ZONE'] == 3

    assert ac_dict[10]['ZONE'] == 4
    assert ac_dict[11]['ZONE'] == 8
    assert ac_dict[12]['ZONE'] == 7
    assert ac_dict[13]['ZONE'] == 6
    assert ac_dict[14]['ZONE'] == 5

    assert ac_dict[0]['FGA'] == 1
    assert ac_dict[0]['FGM'] == 0
    assert ac_dict[1]['FGA'] == 1
    assert ac_dict[1]['FGM'] == 1 

    assert ac_dict[2]['FGA'] == 1
    assert ac_dict[2]['FGM'] == 0
    assert ac_dict[3]['FGA'] == 1
    assert ac_dict[3]['FGM'] == 1 

def test_update_range():
    update_range(ac_df)
    ac_dict = ac_df.to_dict(orient='records')
    
    assert ac_dict[0]['RANGE'] == 'Rim'
    assert ac_dict[1]['RANGE'] == 'Rim'
    
    assert ac_dict[2]['RANGE'] == '3PT'
    assert ac_dict[3]['RANGE'] == '3PT'
    assert ac_dict[4]['RANGE'] == '3PT'
    assert ac_dict[5]['RANGE'] == '3PT'
    assert ac_dict[6]['RANGE'] == '3PT'
    
    assert ac_dict[7]['RANGE'] == 'Mid 2'
    assert ac_dict[8]['RANGE'] == 'Mid 2'
    assert ac_dict[9]['RANGE'] == 'Mid 2'
    
    assert ac_dict[10]['RANGE'] == 'Long 2'
    assert ac_dict[11]['RANGE'] == 'Long 2'
    assert ac_dict[12]['RANGE'] == 'Long 2'
    assert ac_dict[13]['RANGE'] == 'Long 2'
    assert ac_dict[14]['RANGE'] == 'Long 2'

def test_update_lineup():
    update_lineup(sample_df, starter_dict)
    sample_dict = sample_df.to_dict(orient='records')

    assert set(sample_dict[0]['T_65245']) == {'P_205482', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[0]['T_57840']) == {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
    assert set(sample_dict[10]['T_65245']) == {'P_205482', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[10]['T_57840']) == {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
    
    assert set(sample_dict[52]['T_65245']) == {'P_205482', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[52]['T_57840']) == {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
    assert set(sample_dict[53]['T_65245']) == {'P_205482', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[53]['T_57840']) == {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
    
    assert set(sample_dict[54]['T_65245']) == {'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[54]['T_57840']) == {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
    assert set(sample_dict[55]['T_65245']) == {'P_224342', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[55]['T_57840']) == {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
    
    assert set(sample_dict[64]['T_65245']) == {'P_224342', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[64]['T_57840']) == {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
    assert set(sample_dict[65]['T_65245']) == {'P_224342', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[65]['T_57840']) == {'P_272277', 'P_185988', 'P_188667', 'P_258737', 'P_205412'}
    
    assert set(sample_dict[66]['T_65245']) == {'P_224342', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[66]['T_57840']) == {'P_272277', 'P_185988', 'P_258737', 'P_205412'}
    
    assert set(sample_dict[67]['T_65245']) == {'P_224342', 'P_224350', 'P_206446', 'P_194018', 'P_199054'}
    assert set(sample_dict[67]['T_57840']) == {'P_272277', 'P_185988', 'P_258737', 'P_205412', 'P_210544'}
