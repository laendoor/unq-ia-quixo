from dilorenzo_matkorski import Quixo
from easy import Easy

if __name__ == '__main__':
    while True:
        hardPlayer = Quixo()  # 1 | o
        easyPlayer = Quixo(Easy)  # -1 | x
        res_dic = {
            'o': 'Hard',
            'x': 'Easy',
            'Draw': 'Nadie'
        }
        turn = 1
        while True:
            # hard.game.print_board()

            if turn == 1:

                move = hardPlayer.playerPlay()
                easyPlayer.opponentPlay(move)
            else:
                move = easyPlayer.playerPlay()
                hardPlayer.opponentPlay(move)

            turn = turn * -1

            if hardPlayer.game.get_winner():
                # hard.game.print_board()
                winner = hardPlayer.game.get_winner()
                print(f'Ganador: {winner} ({res_dic[winner]})')
                break
