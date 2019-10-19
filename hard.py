import numpy


class Hard(object):

    @staticmethod
    def value(node, i_am):
        players = {-1: 'x', 1: 'o'}

        score = 0

        winner = node.check_for_winner()

        # Devuelvo score minimo si es un tablero donde pierdo
        if winner and node.determine_winner() == players[i_am * -1]:
            return -1000

        # Devuelvo score máximo si es un tablero donde gano
        if winner and node.determine_winner() == players[i_am]:
            return 1000

        # Sumo 1 de score por cada ficha
        tokens = node.board.flatten()
        unique, counts = numpy.unique(tokens, return_counts=True)
        score += (dict(zip(unique, counts)))[i_am]

        # Devuelvo score minimo si es un tablero donde puedo perder en el próximo turno
        winner = node.check_for_winner(4)
        if winner and node.determine_winner(4) == players[i_am * -1]:
            return -1000

        # TODO: Ir tapandole las jugadas el oponente?

        return score
