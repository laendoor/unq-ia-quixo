from quixo import Quixo
from quixo import QuixoGame

if __name__ == '__main__':
    g = QuixoGame()
    alphabeta = Quixo()
    result = alphabeta.alphabeta(g, 1, 10, -10, 1)
    g.print_board()
    print(result)
