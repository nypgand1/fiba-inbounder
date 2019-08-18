from fiba_inbounder.game_parser import FibaGameParser

def test_get_game_teams_json_dataframe_v7():
    df = FibaGameParser.get_game_teams_json_dataframe_v7(event_id='208053', game_unit='24532-18-A')
    
    stats_dict = df.to_dict(orient='records')
    assert stats_dict[0]['Name'] == 'Pauian'
    assert stats_dict[0]['PTS'] == 96
    assert stats_dict[0]['OPP_DR'] == 28
    assert stats_dict[1]['TeamCode'] == 'THA'
    assert stats_dict[0]['TP'] == 200

    #OT1
    df = FibaGameParser.get_game_teams_json_dataframe_v7(event_id='208053', game_unit='24527-B-1')
    stats_dict = df.to_dict(orient='records')
    assert stats_dict[1]['TP'] == 225

if __name__ == '__main__':
    main()
