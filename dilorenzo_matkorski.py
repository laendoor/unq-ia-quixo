#!/usr/bin/python

from random import random
from copy import deepcopy
from quixo import QuixoGame

MAX = 1
MIN = -1
inf = 1000


class Quixo(object):

    def __init__(self):
        self.i_am = None
        self.game = QuixoGame(MAX)

    def playerPlay(self):
        if self.i_am is None:
            self.i_am = MAX
        ab = self.alphabeta(self.game, depth=2, alpha=10, beta=10, player=self.i_am)
        self.game.make_move(ab[0][0], ab[0][1])
        return ab[0]

    def opponentPlay(self, move):
        if self.i_am is None:
            self.i_am = MIN
        self.game.make_move(move[0], move[1])

    @staticmethod
    def game_over(game):
        return game.get_winner() is not None

    @staticmethod
    def h(game):
        return random()

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
            move = None
            for move in self.valid_moves(node):
                next_node = deepcopy(node)
                child = self.play(next_node, move)
                next_score = self.alphabeta(child, depth - 1, alpha, beta, -player)
                best = max(best, next_score[1])
                alpha = max(alpha, best)
                if alpha >= beta:
                    break  # beta cut - off
            return move, best
        else:
            best = inf
            move = None
            for move in self.valid_moves(node):
                next_node = deepcopy(node)
                child = self.play(next_node, move)
                next_score = self.alphabeta(child, depth - 1, alpha, beta, -player)
                best = min(best, next_score[1])
                beta = min(beta, best)
                if alpha >= beta:
                    break  # alpha cut - off
            return move, best
