from six.moves import input
from quixo import InvalidMove
from quixo import Quixo

if __name__ == '__main__':
    turn = 1
    quixo = Quixo()
    while True:
        quixo.game.print_board()
        turn_name = 'o' if turn == 1 else 'x'
        if turn == 1:
            row = input(f'Humano {turn_name} saca ficha: ')
            reinsert = input(f'Humano {turn_name} mete en: ')
            try:
                quixo.opponentPlay((int(row), int(reinsert)))
            except InvalidMove as e:
                print(e.message)
                continue
        else:
            quixo.playerPlay()

        if quixo.game.get_winner():
            quixo.game.print_board()
            print(f'Ganó {quixo.game.get_winner()}')
            break
        turn *= -1
