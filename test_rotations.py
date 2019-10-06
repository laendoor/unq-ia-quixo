from quixo import map_move, InvalidMove, valid_reinsertion_directions, reinsert_from_rot90
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
    assert map_move(13) == (4, 1)
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
