from fiba_inbounder.communicator import FibaCommunicator

def test_get_game_data_v5():
    result = FibaCommunicator.get_game_data_v5(match_id='1143749')
    assert result['tm']['1']['name'] == 'Singapore Slingers'

def test_get_game_team_stats_v7():
    result = FibaCommunicator.get_game_stats_v7(event_id='208053', game_unit='24532-18-A')
    assert result['content']['full']['Competitors'][0]['Name'] == 'Pauian'

def test_get_game_play_by_play_v7():
    result = FibaCommunicator.get_game_play_by_play_v7(event_id='208053', game_unit='24532-18-A', period_id='Q1')
    assert result['content']['full']['Items'][0]['Action'] == 'Start of Game'

def test_get_game_details_v7():
    result = FibaCommunicator.get_game_details_v7(event_id='208153', game_unit='25098-A-3')
    assert result['content']['full']['Competitors']['T_57840']['Name'] == 'Fubon Braves'

if __name__ == '__main__':
    main()
