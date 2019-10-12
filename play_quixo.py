from six.moves import input
from quixo import InvalidMove
from quixo import QuixoGame

if __name__ == '__main__':
    turn = 1
    game = QuixoGame(turn)
    while True:
        game.print_board()
        turn_name = 'o' if turn == 1 else 'x'
        row = input(f'jugador {turn_name} saca ficha: ')
        reinsert = input(f'jugador {turn_name} mete en (N, S, E, W): ')
        try:
            game.make_move(int(row), reinsert)
        except InvalidMove as e:
            print(e.message)
            continue
        if game.get_winner():
            game.print_board()
            print(f'Ganó {game.get_winner()}')
            break
        turn *= -1
