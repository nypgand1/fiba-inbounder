import numpy as np
import pandas as pd

from fiba_inbounder.formulas import update_xy_v7, update_zone, update_range

actions = pd.DataFrame([
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
    {'AC': 'P2', 'SX': '81', 'SY': '104'},]) #Left Elbow Long 2PT
 
def test_update_xy_v7():
    update_xy_v7(actions)
    actions_dict = actions.to_dict(orient='records')
    assert actions_dict[0]['X_SIDELINE_M'] == 7.5
    assert actions_dict[0]['Y_BASELINE_M'] == 1.575

def test_update_zone():
    update_zone(actions)
    actions_dict = actions.to_dict(orient='records')
    
    assert actions_dict[0]['DISTANCE'] == 0
    assert actions_dict[1]['DISTANCE'] == 0.48404387134613663
    assert actions_dict[2]['DISTANCE'] == 7.198480742490043
    assert actions_dict[3]['DISTANCE'] == 6.829005701970896
    
    assert actions_dict[0]['ZONE'] == 0
    assert actions_dict[1]['ZONE'] == 0
    
    assert actions_dict[2]['ZONE'] == 12
    assert actions_dict[3]['ZONE'] == 11
    assert actions_dict[4]['ZONE'] == 9
    assert actions_dict[5]['ZONE'] == 13
    assert actions_dict[6]['ZONE'] == 10
    
    assert actions_dict[7]['ZONE'] == 2
    assert actions_dict[8]['ZONE'] == 1
    assert actions_dict[9]['ZONE'] == 3

    assert actions_dict[10]['ZONE'] == 4
    assert actions_dict[11]['ZONE'] == 8
    assert actions_dict[12]['ZONE'] == 7
    assert actions_dict[13]['ZONE'] == 6
    assert actions_dict[14]['ZONE'] == 5

    assert actions_dict[0]['FGA'] == 1
    assert actions_dict[0]['FGM'] == 0
    assert actions_dict[1]['FGA'] == 1
    assert actions_dict[1]['FGM'] == 1 

    assert actions_dict[2]['FGA'] == 1
    assert actions_dict[2]['FGM'] == 0
    assert actions_dict[3]['FGA'] == 1
    assert actions_dict[3]['FGM'] == 1 

def test_update_range():
    update_range(actions)
    actions_dict = actions.to_dict(orient='records')
    
    assert actions_dict[0]['RANGE'] == 'Rim'
    assert actions_dict[1]['RANGE'] == 'Rim'
    
    assert actions_dict[2]['RANGE'] == '3PT'
    assert actions_dict[3]['RANGE'] == '3PT'
    assert actions_dict[4]['RANGE'] == '3PT'
    assert actions_dict[5]['RANGE'] == '3PT'
    assert actions_dict[6]['RANGE'] == '3PT'
    
    assert actions_dict[7]['RANGE'] == 'Mid 2'
    assert actions_dict[8]['RANGE'] == 'Mid 2'
    assert actions_dict[9]['RANGE'] == 'Mid 2'
    
    assert actions_dict[10]['RANGE'] == 'Long 2'
    assert actions_dict[11]['RANGE'] == 'Long 2'
    assert actions_dict[12]['RANGE'] == 'Long 2'
    assert actions_dict[13]['RANGE'] == 'Long 2'
    assert actions_dict[14]['RANGE'] == 'Long 2'
