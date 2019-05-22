from igra import *
from algo_prisk import MiniMax,AlphaBetta
from hevristike import hevristika_basic
from pprint import pprint


def AutomaticTester(player1,player2,n):
    """
    Avtomatic tester that runs the player 1 using hevristic hev1 against player 2 using hevristic hev2 n times and
    returns the score of format: (player 1 wins, player 2 wins)
    :param player1: Class for player 1 algorithm
    :param player2: Class for player 2 algorithm
    :param n: number of times the algorithm is executed
    :return score; (int, int) of format (player 1 wins , player 2 wins)
    """
    score = [0,0]

    for i in range(n):
        trscore = game_playout(player1,player2)

        score[0] += trscore[0]
        score[1] += trscore[1]

    return score


def game_playout(player1,player2):
    igra = Igra()

    # remember who is who
    P1 = igra.na_potezi
    P2 = nasprotnik(igra.na_potezi)

    stevilo_potez = 0

    print(igra.stanje)

    while igra.stanje[0] != "ZMAGA":
        if stevilo_potez % 5 == 0:
            pprint(igra.plosca)
            print("na potezi: ",igra.na_potezi)
            print()
        stevilo_potez += 1
        if igra.na_potezi == P1:
            # izracuna potezo
            player1.izracunaj_potezo(igra.kopija())

            igra.poteza(*player1.poteza)

            if player1.jemljem[0] != "PRAZNO":
                igra.odstrani_figurico(*player1.jemljem)

            # print(igra.stanje)

        elif igra.na_potezi == P2:
            player2.izracunaj_potezo(igra.kopija())

            igra.poteza(*player2.poteza)

            if player2.jemljem[0] != "PRAZNO":
                igra.odstrani_figurico(*player2.jemljem)

            # print(igra.stanje)
        else:
            raise Exception("Nemoramo odigrati poteze igralca {0}".format(igra.na_potezi))

    if igra.stanje[1] == P1:
        return [1,0]
    else:
        return [0,1]


if __name__ == '__main__':
    alg1 = AlphaBetta
    depth1 = 5
    hev1 = hevristika_basic

    alg2 = MiniMax
    depth2 = 4
    hev2 = hevristika_basic

    player1 = alg1(depth1,hev1)
    player2 = alg2(depth2,hev2)

    AutomaticTester(player1,player2,100)

