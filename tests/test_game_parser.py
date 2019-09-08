from fiba_inbounder.game_parser import FibaGameParser

def test_get_game_stats_dataframe_v7():
    team_df, player_df = FibaGameParser.get_game_stats_dataframe_v7(event_id='208053', game_unit='24532-18-A')
    
    stats_dict = team_df.to_dict(orient='records')
    assert stats_dict[0]['Name'] == 'Pauian'
    assert stats_dict[0]['PTS'] == 96
    assert stats_dict[0]['OPP_DR'] == 28
    assert stats_dict[1]['TeamCode'] == 'THA'
    assert stats_dict[0]['SECS'] == 200 * 60

    #OT1
    team_df, player_df = FibaGameParser.get_game_stats_dataframe_v7(event_id='208053', game_unit='24527-B-1')
    stats_dict = team_df.to_dict(orient='records')
    assert stats_dict[1]['SECS'] == 225 * 60

def test_get_game_details_dict_v7():
    id_table, starter_dict = FibaGameParser.get_game_details_dict_v7(event_id='208153', game_unit='25098-A-3')

    assert id_table['T_57840'] == 'FUB'
    assert id_table['P_205412'] == 'W.Tsai'
    assert {id_table[p] for p in starter_dict['T_65245']} == {'W.Suttisin', 'B.Fields III', 'X.Alexander', 'C.Jakrawan', 'N.Muangboon'}
    assert {id_table[p] for p in starter_dict['T_57840']} == {'J.Lewis', 'P.Chang', 'W.Tsai', 'C.Lin', 'C.Garcia'}

if __name__ == '__main__':
    main()
