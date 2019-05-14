from igra import *


def hevristika_basic(algoritem,igralec):
    stfiguric = algoritem.igra.figurice[igralec]  # Število figuric
    stmlinov = 0  # Število mlinov
    blokirani = 0  # Število blokiranih nasprotnikovih žetonov
    odprtimlini = 0  # Odprt mlin
    dvojnimlini = 0  # Dvojni mlin
    zmag_konf = 0  # Zmagovalna konfiguracija

    # izključno samo v fazi 1 in 3
    zet_2_konf = 0  # 2- zetona konfiguracija
    zet_3_konf = 0  # 3- zetoni konfiguracija (2krat pretimo narediti mlin)

    for trojka in algoritem.igra.kombinacije:
        glej = [algoritem.igra.plosca[el[0]][el[1]] for el in trojka]
        if glej == [igralec, igralec, igralec]:
            stmlinov += 1
        elif glej.count(None) == 1 and glej.count(igralec) == 2:
            if trojka[0] == None:
                praznopolje = 0
            elif trojka[1] == None:
                praznopolje = 1
            else:
                praznopolje = 2
            naspr = False  # preverila bo ali je nasprotnik v blizini
            if algoritem.igra.faza == 0:
                zet_2_konf += 1
            for polje in algoritem.igra.sosedi[trojka[praznopolje]]:
                if algoritem.igra.plosca[polje[0]][polje[1]] == igralec:
                    odprtimlini += 1
                elif algoritem.igra.plosca[polje[0]][polje[1]] == nasprotnik(igralec):
                    naspr = True  # nasprotnik nas lahko blokira
                else:
                    pass
            if nasprotnik == False:
                zmag_konf = 1
        else:
            pass

    for i in range(7):
        for j in range(7):
            if algoritem.igra.plosca[i][j] == nasprotnik(igralec):
                blokiran = True
                for sosednja in algoritem.igra.sosedi[(i, j)]:
                    if algoritem.igra.plosca[sosednja[0]][sosednja[1]] == None:
                        blokiran = False
                if blokiran:
                    blokirani += 1
    # KOEFICIENTI KOLIKO JE KAJ VREDNO IN VRACAMO VREDNOSTI
    if algoritem.igra.faza == 0:
        return 26 * stmlinov + 1 * blokirani + 25 * stfiguric + 12 * zet_2_konf
    elif algoritem.igra.faza == 1 and algoritem.igra.figurice[igralec] != 3:
        return 43 * stmlinov + 10 * blokirani + 20 * stfiguric + 32 * odprtimlini + 958 * zmag_konf
    elif algoritem.igra.faza == 1 and algoritem.igra.figurice[nasprotnik(igralec)] == 4:
        return 35 * stmlinov + 25 * blokirani + 8 * stfiguric + 35 * odprtimlini + 958 * zmag_konf
    else:
        return 30 * stfiguric + 21 * odprtimlini + 20 * stmlinov
