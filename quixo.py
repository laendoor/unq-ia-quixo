import numpy as np
# from collections import namedtuple
# from copy import deepcopy
from mittmcts import Draw


class InvalidMove(RuntimeError):
    def __init__(self, arg):
        self.args = arg


# 01 02 03 04 05
# 16 __ __ __ 06
# 15 __ __ __ 07
# 14 __ __ __ 08
# 13 12 11 10 09
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


# QuixoMove = namedtuple('QuixoMove', ['space', 'player', 'roll'])
#
# boundary_indexes = np.array([(0, i) for i in range(5)] +
#                             [(4, i) for i in range(5)] +
#                             [(i, 0) for i in range(1, 4)] +
#                             [(i, 4) for i in range(1, 4)])
#
# boundary_xs, boundary_ys = boundary_indexes.T
#
#
# def roll_x(position, direction):
#     def roll(board):
#         board[position] = np.roll(board[position], shift=1)
#     return roll
#
#
# def roll_y(position, direction):
#     def roll(board):
#         board[:, position] = np.roll(board[:, position], shift=1)
#     return roll


# end unnecessary to compute every time
class QuixoGame(object):

    # State = namedtuple('QuixoState', ['board', 'current_player', 'winner'])

    def __init__(self, initial_player=1):
        self.board = np.zeros((5, 5), dtype=np.int)
        self.current_player = initial_player
        self.winner = None

    def make_move(self, take_move, put_move, reinsert_from):
        take_move = map_move(take_move)
        put_move = map_move(put_move)

        # Moving validations
        if self.board[take_move] == (self.current_player * -1):
            raise InvalidMove("No podés sacar las fichas de tu oponente")
        if reinsert_from not in valids_reinsert_directions(take_move):
            raise InvalidMove("No podés reinsertar la ficha por ese lugar")

        # Si saqué de la fila 1 o de la fila 5 (casilleros: 1, 2, 3, 4, 5, 13, 12, 11, 10, 9)
        if take_move[0] in [0, 4]:
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
        # Creo que se podría mejorar, pero es básicamente la idea...
        # TODO hacer lo mismo para las columnas
        # Algo que se podría hacer es transponer la matriz np.rot90(self.board)
        # y usar lo mismo que arriba, pero teniendo cuidado con los reinsert_from




        # new_board = deepcopy(state.board)
        # self.board[move.space[0], move.space[1]] = move.player
        # move.roll(self.board)


        self.current_player *= -1
        self.winner = self.determine_winner() if self.check_for_winner() else None

    # def get_moves(self):
    #     blocks = np.where(
    #         np.logical_or(
    #             self.board[boundary_xs, boundary_ys] == 0,
    #             self.board[boundary_xs, boundary_ys] == self.current_player
    #         )
    #     )[0]
    #
    #     bxs = boundary_xs[blocks]
    #     bys = boundary_ys[blocks]
    #
    #     moves = list()
    #     for bx, by in zip(bxs, bys):
    #         moves.extend([
    #             QuixoMove((bx, by), self.current_player, roll_x(bx, 1)),
    #             QuixoMove((bx, by), self.current_player, roll_x(bx, -1)),
    #             QuixoMove((bx, by), self.current_player, roll_y(by, 1)),
    #             QuixoMove((bx, by), self.current_player, roll_y(by, -1))
    #         ])
    #     return False, moves

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
