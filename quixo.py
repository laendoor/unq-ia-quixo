import numpy as np


class InvalidMove(RuntimeError):
    def __init__(self, message):
        self.message = str(message)


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
        9: (4, 4), 10: (4, 3), 11: (4, 2), 12: (4, 1), 13: (4, 0),
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


def map_rot90_take_move(take_move):
    moves = {
        (1, 0): (4, 1),
        (2, 0): (4, 2),
        (3, 0): (4, 3),
        (1, 4): (0, 1),
        (2, 4): (0, 2),
        (3, 4): (0, 3),
    }
    tuple = (take_move[0], take_move[1])
    return moves[tuple]


def map_reinsert(take, reinsert):
    _map = {
        (1, 5): "E", (1, 13): "S",
        (2, 1): "W", (2, 5): "E", (2, 12): "S",
        (3, 1): "W", (3, 5): "E", (3, 11): "S",
        (4, 1): "W", (4, 5): "E", (4, 10): "S",
        (5, 1): "W", (5, 9): "S",
        (6, 5): "N", (6, 9): "S", (6, 16): "W",
        (7, 5): "N", (7, 9): "S", (7, 15): "W",
        (8, 5): "N", (8, 9): "S", (8, 14): "W",
        (9, 5): "N", (5, 13): "W",
        (10, 9): "E", (10, 13): "W", (10, 4): "N",
        (11, 9): "E", (11, 13): "W", (11, 3): "N",
        (12, 9): "E", (12, 13): "W", (12, 3): "N",
        (13, 1): "N", (13, 9): "E",
        (14, 1): "N", (14, 13): "S", (14, 8): "E",
        (15, 1): "N", (15, 13): "S", (15, 7): "E",
        (16, 1): "N", (16, 13): "S", (16, 6): "E"
    }
    if (take, reinsert) not in _map:
        raise InvalidMove("No se puede hacer esa jugada")
    return _map[(take, reinsert)]


def map_reinsert_reverse(take, reinsert_coord):
    _map = {
        (1, "E"): 5, (1, "S"): 13,
        (2, "W"): 1, (2, "E"): 5, (2, "S"): 12,
        (3, "W"): 1, (3, "E"): 5, (3, "S"): 11,
        (4, "W"): 1, (4, "E"): 5, (4, "S"): 10,
        (5, "W"): 1, (5, "S"): 9,
        (6, "N"): 5, (6, "S"): 9, (6, "W"): 16,
        (7, "N"): 5, (7, "S"): 9, (7, "W"): 15,
        (8, "N"): 5, (8, "S"): 9, (8, "W"): 14,
        (9, "N"): 5, (5, "W"): 13,
        (10, "E"): 9, (10, "W"): 13, (10, "N"): 4,
        (11, "E"): 9, (11, "W"): 13, (11, "N"): 3,
        (12, "E"): 9, (12, "W"): 13, (12, "N"): 3,
        (13, "N"): 1, (13, "E"): 9,
        (14, "N"): 1, (14, "S"): 13, (14, "E"): 8,
        (15, "N"): 1, (15, "S"): 13, (15, "E"): 7,
        (16, "N"): 1, (16, "S"): 13, (16, "E"): 6
    }
    if (take, reinsert_coord) not in _map:
        raise InvalidMove("Esa coordenada no va")
    return take, _map[(take, reinsert_coord)]


class QuixoGame(object):

    def __init__(self, initial_player=1):
        self.board = np.zeros((5, 5), dtype=np.int)
        self.current_player = initial_player
        self.winner = None

    def make_move(self, take_move, reinsert_from):
        reinsert_from = map_reinsert(take_move, reinsert_from);
        reinsert_from = reinsert_from.upper()
        take_move = map_move(take_move)
        self._assert_valid_move(take_move, reinsert_from)

        # Si tome 1, 2, 3, 4, 5, 9, 10, 11, 12 o 13:
        if take_move[0] in [0, 4]:
            self._reinsert(take_move, reinsert_from)

        # Si tome: 6, 7, 8, 14, 15 o 16
        if take_move[0] in [1, 2, 3]:
            self.board = np.rot90(self.board, 1)  # Rotate 90° anticlockwise
            self._reinsert(map_rot90_take_move(take_move), reinsert_from_rot90(reinsert_from))
            self.board = np.rot90(self.board, -1)  # Rotate 90° counterclockwise (rollback to original position)

        self.current_player *= -1
        self.winner = self.determine_winner() if self.check_for_winner() else None

    def _reinsert(self, take_move, reinsert_from):
        # Y quiero reinsertar desde el Norte o el Sur
        # Shifteo la columna
        if reinsert_from in ["S", "N"]:
            shift = -1 if reinsert_from == "S" else 1
            self.board[take_move] = self.current_player
            self.board[:, take_move[1]] = np.roll(self.board[:, take_move[1]], shift=shift)
        # Y quiero reinsertar desde Oeste o Este
        # Separa la fila en dos (sin incluir la sacada) y la reinserto desde atrás o adelante
        if reinsert_from in ["W", "E"]:
            left = self.board[take_move[0]][:take_move[1]]
            right = self.board[take_move[0]][take_move[1]+1:]
            new_line = np.concatenate((left, right))
            if reinsert_from == "W":
                new_line = np.concatenate(([self.current_player], new_line))
            else:
                new_line = np.concatenate((new_line, [self.current_player]))
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
            winner_map = ['Draw', 'o', 'x']
            return winner_map[winner]
    
    def get_winner(self):
        return self.winner

    def current_player(self):
        return self.current_player

    #        1  2  3  4  5
    #    ++ == == == == == ++
    #    || __ __ __ __ __ ||
    # 16 || __ __ __ __ __ || 6
    # 15 || __ __ __ __ __ || 7
    # 14 || __ __ __ __ __ || 8
    # 13 || __ __ __ __ __ || 9
    #    ++ == == == == == ++
    #          12 11 10
    def print_board(self):
        l1 = ' '.join(map(self.print_position, self.board[0]))
        l2 = ' '.join(map(self.print_position, self.board[1]))
        l3 = ' '.join(map(self.print_position, self.board[2]))
        l4 = ' '.join(map(self.print_position, self.board[3]))
        l5 = ' '.join(map(self.print_position, self.board[4]))
        print("        1  2  3  4  5")
        print("    ++ == == == == == ++")
        print(f"    || { l1 } ||  ")
        print(f" 16 || { l2 } || 6")
        print(f" 15 || { l3 } || 7")
        print(f" 14 || { l4 } || 8")
        print(f" 13 || { l5 } || 9")
        print("    ++ == == == == == ++")
        print("          12 11 10   ")

    @staticmethod
    def print_position(player):
        if player == 1:
            return ' o'
        elif player == -1:
            return ' x'
        else:
            return '  '