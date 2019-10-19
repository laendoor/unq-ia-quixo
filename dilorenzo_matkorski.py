#!/usr/bin/python

from copy import deepcopy

from hard import Hard
from quixo import QuixoGame

MAX = 1
MIN = -1
inf = 100000


class Quixo(object):

    def __init__(self, heuristic=Hard):
        self.i_am = None
        self.game = QuixoGame(MAX)
        self.heuristic = heuristic

    def playerPlay(self):
        if self.i_am is None:
            self.i_am = MAX
        ab = self.alphabeta(self.game, depth=3, alpha=-inf, beta=inf, player=self.i_am)
        self.game.make_move(ab[0][0], ab[0][1])
        return ab[0]

    def opponentPlay(self, move):
        if self.i_am is None:
            self.i_am = MIN
        self.game.make_move(move[0], move[1])

    @staticmethod
    def game_over(game):
        return game.get_winner() is not None

    def h(self, game):
        return self.heuristic.value(game, self.i_am)

    @staticmethod
    def valid_moves(game):
        return game.valid_moves()

    @staticmethod
    def play(game, move):
        game.make_move(move[0], move[1])
        return game

    def alphabeta(self, node, depth, alpha, beta, player):
        if depth == 0 or self.game_over(node):
            return None, self.h(node)
        if player == MAX:
            best = -inf
            best_move = None
            valids = self.valid_moves(node)
            for move in valids:
                next_node = deepcopy(node)
                child = self.play(next_node, move)
                _, next_score = self.alphabeta(child, depth - 1, alpha, beta, -player)

                if next_score > best:
                    best_move = move
                best = max(best, next_score)
                alpha = max(alpha, best)
                if alpha >= beta:
                    break  # beta cut - off
            return best_move, best
        else:
            best = inf
            best_move = None
            valids = self.valid_moves(node)
            for move in valids:
                next_node = deepcopy(node)
                child = self.play(next_node, move)
                _, next_score = self.alphabeta(child, depth - 1, alpha, beta, -player)

                if next_score < best:
                    best_move = move
                best = min(best, next_score)
                beta = min(beta, best)
                if alpha >= beta:
                    break  # alpha cut - off
            return best_move, best
