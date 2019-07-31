from fiba_inbounder.communicator import FibaCommunicator

def test_get_game():
    game_id = '1143749'
    result = FibaCommunicator.get_game(game_id)
    assert result['tm']['1']['name'] == 'Singapore Slingers'

if __name__ == '__main__':
    main()
