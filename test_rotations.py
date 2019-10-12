from quixo import *
import pytest


def test_reinsert_from_rotation():
    assert reinsert_from_rot90("N") == "W"
    assert reinsert_from_rot90("W") == "S"
    assert reinsert_from_rot90("S") == "E"
    assert reinsert_from_rot90("E") == "N"


def test_valid_reinsertion_directions():
    assert valid_reinsertion_directions((0, 0)) == ["S", "E"]
    assert valid_reinsertion_directions((0, 1)) == ["S", "E", "W"]
    assert valid_reinsertion_directions((0, 2)) == ["S", "E", "W"]
    assert valid_reinsertion_directions((0, 3)) == ["S", "E", "W"]
    assert valid_reinsertion_directions((0, 4)) == ["S", "W"]
    assert valid_reinsertion_directions((1, 0)) == ["N", "S", "E"]
    assert valid_reinsertion_directions((1, 4)) == ["N", "S", "W"]
    assert valid_reinsertion_directions((2, 0)) == ["N", "S", "E"]
    assert valid_reinsertion_directions((2, 4)) == ["N", "S", "W"]
    assert valid_reinsertion_directions((3, 0)) == ["N", "S", "E"]
    assert valid_reinsertion_directions((3, 4)) == ["N", "S", "W"]
    assert valid_reinsertion_directions((4, 0)) == ["N", "E"]
    assert valid_reinsertion_directions((4, 1)) == ["N", "E", "W"]
    assert valid_reinsertion_directions((4, 2)) == ["N", "E", "W"]
    assert valid_reinsertion_directions((4, 3)) == ["N", "E", "W"]
    assert valid_reinsertion_directions((4, 4)) == ["N", "W"]


def test_map_moves():
    assert map_move(1) == (0, 0)
    assert map_move(2) == (0, 1)
    assert map_move(3) == (0, 2)
    assert map_move(4) == (0, 3)
    assert map_move(5) == (0, 4)
    assert map_move(6) == (1, 4)
    assert map_move(7) == (2, 4)
    assert map_move(8) == (3, 4)
    assert map_move(9) == (4, 4)
    assert map_move(10) == (4, 3)
    assert map_move(11) == (4, 2)
    assert map_move(12) == (4, 1)
    assert map_move(13) == (4, 0)
    assert map_move(14) == (3, 0)
    assert map_move(15) == (2, 0)
    assert map_move(16) == (1, 0)
    with pytest.raises(InvalidMove):
        map_move(0)
    with pytest.raises(InvalidMove):
        map_move(17)


def test_board_rotation():
    original_board = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ]
    rotated_board = [
        [5, 10, 15, 20, 25],
        [4, 9, 14, 19, 24],
        [3, 8, 13, 18, 23],
        [2, 7, 12, 17, 22],
        [1, 6, 11, 16, 21],
    ]
    original_board_rotated = np.rot90(original_board, 1)
    rotated_board_rotated = np.rot90(rotated_board, -1)
    for i in range(0, 4):
        for j in range(0, 4):
            assert original_board_rotated[i][j] == rotated_board[i][j]
            assert rotated_board_rotated[i][j] == original_board[i][j]


def assert_array_equal(arr1, arr2):
    for i in range(0, 5):
        for j in range(0, 5):
            assert arr1[i][j] == arr2[i][j]


def board_after_playing(player, token, direction, board=None):
    game = QuixoGame(player)
    if board is None:
        board = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]]
    game.board = np.array(board)
    game.make_move(token, direction)
    return game.board.tolist()


def test_initial_board_insertion_1_S():
    played_board = board_after_playing(1, 1, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_1_N():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 1, 'N')


def test_initial_board_insertion_1_E():
    played_board = board_after_playing(1, 1, 'E')
    expected_board = [[0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_1_W():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 1, 'W')


def test_initial_board_insertion_2_S():
    played_board = board_after_playing(1, 2, 'S')

    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_2_N():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 2, 'N')


def test_initial_board_insertion_2_E():
    played_board = board_after_playing(1, 2, 'E')
    expected_board = [[0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_2_W():
    played_board = board_after_playing(1, 2, 'W')
    expected_board = [[1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_3_S():
    played_board = board_after_playing(1, 3, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_3_N():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 3, 'N')


def test_initial_board_insertion_3_E():
    played_board = board_after_playing(1, 3, 'E')
    expected_board = [[0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_3_W():
    played_board = board_after_playing(1, 3, 'W')
    expected_board = [[1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_4_S():
    played_board = board_after_playing(1, 4, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_4_N():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 4, 'N')


def test_initial_board_insertion_4_E():
    played_board = board_after_playing(1, 4, 'E')
    expected_board = [[0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_4_W():
    played_board = board_after_playing(1, 4, 'W')
    expected_board = [[1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_5_S():
    played_board = board_after_playing(1, 5, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_5_N():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 5, 'N')


def test_initial_board_insertion_5_E():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 5, 'E')


def test_initial_board_insertion_5_W():
    played_board = board_after_playing(1, 5, 'W')
    expected_board = [[1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_6_S():
    played_board = board_after_playing(1, 6, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_6_N():
    played_board = board_after_playing(1, 6, 'N')
    expected_board = [[0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_6_E():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 6, 'E')


def test_initial_board_insertion_6_W():
    played_board = board_after_playing(1, 6, 'W')
    expected_board = [[0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_7_S():
    played_board = board_after_playing(1, 7, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_7_N():
    played_board = board_after_playing(1, 7, 'N')
    expected_board = [[0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_7_E():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 7, 'E')


def test_initial_board_insertion_7_W():
    played_board = board_after_playing(1, 7, 'W')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_8_S():
    played_board = board_after_playing(1, 8, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_8_N():
    played_board = board_after_playing(1, 8, 'N')
    expected_board = [[0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_8_E():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 8, 'E')


def test_initial_board_insertion_8_W():
    played_board = board_after_playing(1, 8, 'W')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_9_S():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 9, 'S')


def test_initial_board_insertion_9_N():
    played_board = board_after_playing(1, 9, 'N')
    expected_board = [[0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_9_E():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 9, 'E')


def test_initial_board_insertion_9_W():
    played_board = board_after_playing(1, 9, 'W')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_10_S():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 10, 'S')


def test_initial_board_insertion_10_N():
    played_board = board_after_playing(1, 10, 'N')
    expected_board = [[0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_10_E():
    played_board = board_after_playing(1, 10, 'E')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_10_W():
    played_board = board_after_playing(1, 10, 'W')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_11_S():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 11, 'S')


def test_initial_board_insertion_11_N():
    played_board = board_after_playing(1, 11, 'N')
    expected_board = [[0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_11_E():
    played_board = board_after_playing(1, 11, 'E')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_11_W():
    played_board = board_after_playing(1, 11, 'W')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_12_S():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 12, 'S')


def test_initial_board_insertion_12_N():
    played_board = board_after_playing(1, 12, 'N')
    expected_board = [[0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_12_E():
    played_board = board_after_playing(1, 12, 'E')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_12_W():
    played_board = board_after_playing(1, 12, 'W')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_13_S():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 13, 'S')


def test_initial_board_insertion_13_N():
    played_board = board_after_playing(1, 13, 'N')
    expected_board = [[1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_13_E():
    played_board = board_after_playing(1, 13, 'E')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_13_W():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 13, 'W')


def test_initial_board_insertion_14_S():
    played_board = board_after_playing(1, 14, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_14_N():
    played_board = board_after_playing(1, 14, 'N')
    expected_board = [[1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_14_E():
    played_board = board_after_playing(1, 14, 'E')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_14_W():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 14, 'W')


def test_initial_board_insertion_15_S():
    played_board = board_after_playing(1, 15, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_15_N():
    played_board = board_after_playing(1, 15, 'N')
    expected_board = [[1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_15_E():
    played_board = board_after_playing(1, 15, 'E')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_15_W():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 15, 'W')


def test_initial_board_insertion_16_S():
    played_board = board_after_playing(1, 16, 'S')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_16_N():
    played_board = board_after_playing(1, 16, 'N')
    expected_board = [[1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_16_E():
    played_board = board_after_playing(1, 16, 'E')
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
    assert_array_equal(played_board, expected_board)


def test_initial_board_insertion_16_W():
    with pytest.raises(InvalidMove):
        board_after_playing(1, 16, 'W')


def test_initial_advanced_move():
    initial_board = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, -1, 1],
                     [0, 0, 0, -1, 1]]
    played_board = board_after_playing(-1, 7, 'W', initial_board)
    expected_board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [-1, 0, 0, 0, 0],
                      [0, 0, 0, -1, 1],
                      [0, 0, 0, -1, 1]]
    assert_array_equal(played_board, expected_board)
