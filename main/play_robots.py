from quixo import Easy, Quixo

if __name__ == '__main__':
    while True:
        plays = 1
        hardPlayer = Quixo()  # 1 | o
        easyPlayer = Quixo(Easy)  # -1 | x
        res_dic = {
            'o': 'Hard',
            'x': 'Easy',
            'Draw': 'Nadie'
        }
        turn = 1
        while True:
            # hardPlayer.game.print_board()

            if turn == 1:

                move = hardPlayer.playerPlay()
                easyPlayer.opponentPlay(move)
            else:
                move = easyPlayer.playerPlay()
                hardPlayer.opponentPlay(move)

            turn = turn * -1
            plays +=1
            if hardPlayer.game.get_winner():
                # hardPlayer.game.print_board()
                winner = hardPlayer.game.get_winner()
                print(f'Ganador: {winner} ({res_dic[winner]}) en {plays} jugadas')
                break
