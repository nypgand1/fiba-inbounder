# -*- coding: utf-8 -*-
from fiba_inbounder.game_parser import FibaGameParser

def test_get_game_stats_dataframe_pleague():
    team_stats_df, player_stats_df, team_id_away, team_id_home, id_table = FibaGameParser.get_game_stats_dataframe_pleague(game_id='2')
    stats_dict = team_stats_df.to_dict(orient='records')
    assert stats_dict[0]['Name'] == u'桃園領航猿'
    assert stats_dict[0]['OPP_DR'] == 39
    assert stats_dict[0]['SECS'] == 14400
    assert stats_dict[0]['Periods'][0] == {'Id': 'Q1', 'Score': 24}
    assert stats_dict[0]['Periods'][1] == {'Id': 'Q2', 'Score': 14}
    assert stats_dict[0]['Periods'][2] == {'Id': 'Q3', 'Score': 20}
    assert stats_dict[0]['Periods'][3] == {'Id': 'Q4', 'Score': 9}
    assert stats_dict[0]['PeriodIdList'] == ['Q1', 'Q2', 'Q3', 'Q4'] 
    assert stats_dict[1]['TeamCode'] == u'臺北富邦勇士'
    assert team_id_away == 1
    assert team_id_home == 2
    assert id_table[1] == u'賴廷恩'
    
def test_get_game_stats_dataframe_v5():
    team_stats_df, player_stats_df, starter_dict, pbp_df, shot_df = FibaGameParser.get_game_data_dataframe_v5(match_id='987140')
    
    stats_dict = team_stats_df.to_dict(orient='records')
    assert stats_dict[0]['Name'] == 'Saigon Heat'
    assert stats_dict[0]['OPP_DR'] == 40
    assert stats_dict[0]['SECS'] == 13500
    assert stats_dict[0]['tot_sMinutes'] == '225:00'
    assert stats_dict[0]['Periods'][0] == {'Id': 'Q1', 'Score': 22}
    assert stats_dict[0]['Periods'][1] == {'Id': 'Q2', 'Score': 17}
    assert stats_dict[0]['Periods'][2] == {'Id': 'Q3', 'Score': 11}
    assert stats_dict[0]['Periods'][3] == {'Id': 'Q4', 'Score': 24}
    assert stats_dict[0]['Periods'][4] == {'Id': 'OT', 'Score': 11}
    assert stats_dict[0]['PeriodIdList'] == ['Q1', 'Q2', 'Q3', 'Q4', 'OT']
    assert stats_dict[1]['TeamCode'] == 'FMD'
    assert stats_dict[1]['A_FBP'] == 12
    assert stats_dict[1]['A_PAT'] == 19
    assert stats_dict[1]['A_PFB'] == 13
    assert stats_dict[1]['A_PIP'] == 52
    assert stats_dict[1]['A_SCP'] == 16
    assert stats_dict[1]['PeriodIdList'] == ['Q1', 'Q2', 'Q3', 'Q4', 'OT']

    assert starter_dict == {
            'FMD': {'06 H.LEE','23 K.CHIEN','31 W.ARTINO','33 M.MILLER','40 T.GLASS'},
            'SGH': {'01 T.HUGHES','11 T.DINH','12 J.YOUNG','13 M.BURNATOWSKI','33 K.BARONE'}}

def test_get_game_stats_dataframe_v7():
    team_stats_df, player_stats_df = FibaGameParser.get_game_stats_dataframe_v7(event_id='208053', game_unit='24532-18-A')
    
    stats_dict = team_stats_df.to_dict(orient='records')
    assert stats_dict[0]['Name'] == 'Pauian'
    assert stats_dict[0]['PTS'] == 96
    assert stats_dict[0]['OPP_DR'] == 28
    assert stats_dict[1]['TeamCode'] == 'THA'
    assert stats_dict[0]['SECS'] == 200 * 60

    #OT1
    team_df, player_stats_df = FibaGameParser.get_game_stats_dataframe_v7(event_id='208053', game_unit='24527-B-1')
    stats_dict = team_df.to_dict(orient='records')
    assert stats_dict[1]['SECS'] == 225 * 60

def test_get_game_details_dict_v7():
    id_table, starter_dict = FibaGameParser.get_game_details_dict_v7(event_id='208153', game_unit='25098-A-3')

    assert id_table['T_57840'] == 'FUB'
    assert id_table['P_205412'] == '14 W.Tsai'
    assert {id_table[p] for p in starter_dict['T_65245']} == {'02 W.Suttisin', '23 B.Fields III', '15 X.Alexander', '31 C.Jakrawan', '27 N.Muangboon'}
    assert {id_table[p] for p in starter_dict['T_57840']} == {'18 J.Lewis', '07 P.Chang', '14 W.Tsai', '15 C.Lin', '36 C.Garcia'}

if __name__ == '__main__':
    main()
