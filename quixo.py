import numpy as np
# from collections import namedtuple
# from copy import deepcopy
from mittmcts import Draw


class InvalidMove(RuntimeError):
    def __init__(self, arg):
        self.args = arg


#       0  1  2  3  4
#   ++ == == == == ==
# 0 ||  1  2  3  4  5
# 1 || 16 __ __ __  6
# 2 || 15 __ __ __  7
# 3 || 14 __ __ __  8
# 4 || 13 12 11 10  9
def map_move(move_number):
    moves = {
        1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0, 4),
        6: (1, 4), 7: (2, 4), 8: (3, 4),
        9: (4, 4), 10: (4, 3), 11: (4, 2), 12: (4, 1), 13: (4, 1),
        14: (3, 0), 15: (2, 0), 16: (1, 0),
    }
    if move_number not in moves:
        raise InvalidMove("Esa posición no pertenece al tablero o bien es interna")

    return moves[move_number]


def valid_reinsertion_directions(taken_move):
    directions = {
        (0, 0): ['',  "S", "E",  ""],
        (0, 1): ['',  "S", "E", "W"],
        (0, 2): ['',  "S", "E", "W"],
        (0, 3): ['',  "S", "E", "W"],
        (0, 4): ['',  "S",  '', "W"],
        (1, 0): ["N", "S", "E",  ''],
        (1, 4): ["N", "S",  '', "W"],
        (2, 0): ["N", "S", "E",  ''],
        (2, 4): ["N", "S",  '', "W"],
        (3, 0): ["N", "S", "E",  ''],
        (3, 4): ["N", "S",  '', "W"],
        (4, 0): ["N",  '', "E",  ''],
        (4, 1): ["N",  '', "E", "W"],
        (4, 2): ["N",  '', "E", "W"],
        (4, 3): ["N",  '', "E", "W"],
        (4, 4): ["N",  '',  '', "W"],
    }
    return list(filter(None, directions[taken_move]))


# Rotate coordinates 90° anticlockwise
def reinsert_from_rot90(reinsert_from):
    map_directions = {"N": "W", "W": "S", "S": "E", "E": "N"}
    return map_directions[reinsert_from]


class QuixoGame(object):

    def __init__(self, initial_player=1):
        self.board = np.zeros((5, 5), dtype=np.int)
        self.current_player = initial_player
        self.winner = None

    def make_move(self, take_move, reinsert_from):
        take_move = map_move(take_move)
        self._assert_valid_move(take_move, reinsert_from)

        # Si saqué de la fila 1 o de la fila 5 (casilleros: 1, 2, 3, 4, 5, 9, 10, 11, 12, 13)
        if take_move[0] in [0, 4]:
            self._reinsert(take_move, reinsert_from)

        # Si saqué de la columna 1 o de la columna 5 (casilleros: 6, 7, 8, 14, 15, 16)
        if take_move[0] in [1, 2, 3]:
            np.rot90(self.board, 1)     # Rotate 90° anticlockwise
            self._reinsert(take_move, reinsert_from_rot90(reinsert_from))
            np.rot90(self.board, -1)    # Rotate 90° counterclockwise (rollback to original position)

        self.current_player *= -1
        self.winner = self.determine_winner() if self.check_for_winner() else None

    def _reinsert(self, take_move, reinsert_from):
        # Y quiero reinsertar desde el Norte o el Sur
        # Shifteo la columna
        if reinsert_from in ["S", "N"]:
            shift = 1 if reinsert_from == "S" else -1
            self.board[take_move] = self.current_player
            self.board[:, take_move[1]] = np.roll(self.board[:, take_move[1]], shift=shift)
        # Y quiero reinsertar desde Oeste o Este
        # Separa la fila en dos (sin incluir la sacada) y la reinserto desde atrás o adelante
        if reinsert_from in ["W", "E"]:
            left = self.board[take_move[0]][:take_move[0]]
            right = self.board[take_move[0]][take_move[0]:]
            new_line = left + right
            if reinsert_from == "W":
                new_line = [self.current_player] + new_line
            else:
                new_line = new_line + [self.current_player]
            self.board[take_move[0]] = new_line

    def _assert_valid_move(self, taken_move, reinsert_from):
        # Moving validations
        if self.board[taken_move] == (self.current_player * -1):
            raise InvalidMove("No podés sacar las fichas de tu oponente")
        if reinsert_from not in valid_reinsertion_directions(taken_move):
            raise InvalidMove("No podés reinsertar la ficha por ese lugar")

    def check_for_winner(self):
        return any(abs(np.sum(self.board, axis=0)) == 5) or\
            any(abs(np.sum(self.board, axis=1)) == 5) or\
            abs(np.sum((self.board.diagonal()))) == 5 or\
            abs(np.sum((self.board[::-1].diagonal()))) == 5

    def determine_winner(self):
        winning_players = list()
        row_sums = np.sum(self.board, axis=0)
        win_rows = np.where(np.abs(row_sums) == 5)[0]
        if len(win_rows) > 0:
            winning_players.extend(np.sign(row_sums[win_rows]))
        
        col_sums = np.sum(self.board, axis=1)
        win_cols = np.where(np.abs(col_sums) == 5)[0]
        if len(win_cols) > 0:
            winning_players.extend(np.sign(col_sums[win_cols]))

        diag0 = np.sum((self.board.diagonal()))
        diag1 = np.sum((self.board[::-1].diagonal()))
        for diag in [diag0, diag1]:
            if abs(diag) == 5:
                winning_players.append(np.sign(diag))

        winning_players = set(winning_players)
        if len(winning_players) > 1:
            return 'Draw'
        else:
            winner = winning_players.pop()
            winner_map = [Draw, 'o', 'x']
            return winner_map[winner]
    
    def get_winner(self):
        return self.winner

    def current_player(self):
        return self.current_player

    def print_board(self):
        char_map = np.array([' ', 'o', 'x'])
        print(' ' + ' '.join(map(str, np.arange(5))) +
              '\n' + '_' * (5 * 2 + 2))
        for num_row, row in enumerate(self.board):
            print(str(num_row) + '|' + '|'.join(char_map[row]) + '|')
        print('_' * (5 * 2 + 2))
