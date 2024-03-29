__author__ = 'LukaAvbreht'

from copy import deepcopy

IGRALEC_ENA = "B"
IGRALEC_DVA = "C"


def nasprotnik(igralec):
    """ Pove nasprotnega igralca. Koristno pri metodi poteza. """
    if igralec == IGRALEC_ENA:
        return IGRALEC_DVA
    elif igralec == IGRALEC_DVA:
        return IGRALEC_ENA
    else:
        1 / 0  # Sesuje igro, saj ni druge možne situacije.


class Igra():
    """Program namenjen logiki in pravilom igre"""

    def __init__(self):  # remove nepotrebna polja
        self.plosca = [
            [None, " ", " ", None, " ", " ", None],
            [" ", None, " ", None, " ", None, " "],
            [" ", " ", None, None, None, " ", " "],
            [None, None, None, " ", None, None, None],
            [" ", " ", None, None, None, " ", " "],
            [" ", None, " ", None, " ", None, " "],
            [None, " ", " ", None, " ", " ", None]
        ]
        # None polja so prosta polja, " " so samo fillerji.
        self.na_potezi = IGRALEC_ENA

        self.figurice = {IGRALEC_ENA: 0, IGRALEC_DVA: 0}
        # Sproti spremljajo žetone

        self.faza = 0

        self.postavljenih = 0  # števec ki steje koliko figur je ze bilo postavljenih

        # self.faza = 0  --> Faza postavljanja figuric
        # self.faza = 1  --> Faza premikanja figuric

        self.zgodovina = []
        # (kam, od kje, jemanje?, kdonapotezi), Tupli dolžine 7

        self.stanje = ("V TEKU", None)
        # moznosti tega stanja so : ni konec, zmaga
        # ("V TEKU", None)
        # ("ZMAGA", Igralec)

        self.mlin = False
        # pove ali smo postavili mlin

        self.sosedi = {
            (0, 0): [(0, 3), (3, 0)],
            (0, 6): [(0, 3), (3, 6)],
            (6, 0): [(3, 0), (6, 3)],
            (6, 6): [(6, 3), (3, 6)],

            (2, 2): [(2, 3), (3, 2)],
            (2, 4): [(2, 3), (3, 4)],
            (4, 2): [(3, 2), (4, 3)],
            (4, 4): [(4, 3), (3, 4)],

            (1, 1): [(1, 3), (3, 1)],
            (1, 5): [(1, 3), (3, 5)],
            (5, 1): [(5, 3), (3, 1)],
            (5, 5): [(5, 3), (3, 5)],

            (0, 3): [(0, 0), (0, 6), (1, 3)],
            (3, 0): [(0, 0), (6, 0), (3, 1)],
            (6, 3): [(6, 0), (6, 6), (5, 3)],
            (3, 6): [(0, 6), (6, 6), (3, 5)],

            (3, 2): [(3, 1), (2, 2), (4, 2)],
            (3, 4): [(2, 4), (4, 4), (3, 5)],
            (4, 3): [(4, 2), (4, 4), (5, 3)],
            (2, 3): [(2, 2), (2, 4), (1, 3)],

            (3, 1): [(3, 0), (3, 2), (1, 1), (5, 1)],
            (1, 3): [(1, 1), (1, 5), (2, 3), (0, 3)],
            (3, 5): [(3, 4), (3, 6), (1, 5), (5, 5)],
            (5, 3): [(5, 1), (5, 5), (4, 3), (6, 3)],
        }
        self.kombinacije = [
            [(0, 0), (0, 3), (0, 6)],
            [(6, 0), (6, 3), (6, 6)],
            [(1, 1), (1, 3), (1, 5)],
            [(5, 1), (5, 3), (5, 5)],
            [(2, 2), (2, 3), (2, 4)],
            [(4, 2), (4, 3), (4, 4)],
            [(3, 0), (3, 1), (3, 2)],
            [(3, 4), (3, 5), (3, 6)],
            # Navpične
            [(0, 0), (3, 0), (6, 0)],
            [(0, 6), (3, 6), (6, 6)],
            [(1, 1), (3, 1), (5, 1)],
            [(1, 5), (3, 5), (5, 5)],
            [(2, 2), (3, 2), (4, 2)],
            [(2, 4), (3, 4), (4, 4)],
            [(0, 3), (1, 3), (2, 3)],
            [(4, 3), (5, 3), (6, 3)]]

    def kopija(self):
        """ Naredi novo kopijo igre z vsemi pomembnimi podatki. """
        copy = Igra()
        copy.plosca = [self.plosca[i][:] for i in range(7)]
        copy.na_potezi = self.na_potezi
        copy.faza = self.faza
        copy.postavljenih = self.postavljenih
        copy.figurice = self.figurice.copy()  # hard copy
        return copy

    def razveljavi(self):
        """ Razveljavi zadnjo potezo. """
        i, j, a, b, c, d, kdonapotezi = self.zgodovina.pop(-1)
        self.plosca[i][j] = None
        if a == "PRAZNO" and b == "PRAZNO":
            self.postavljenih -= 1
            if self.postavljenih < 18:
                self.faza = 0
            else:
                self.faza = 1
            self.figurice[kdonapotezi] -= 1
        else:
            self.plosca[a][b] = kdonapotezi
        if c == "PRAZNO" and d == "PRAZNO":
            pass
        else:
            self.plosca[c][d] = nasprotnik(kdonapotezi)
            self.figurice[nasprotnik(kdonapotezi)] += 1
        self.na_potezi = kdonapotezi

    def razveljavi_jemanje(self):
        """ Razveljavi zadnje jemanje. """
        c = self.zgodovina[-1][4]
        d = self.zgodovina[-1][5]
        if c == "PRAZNO" and d == "PRAZNO":
            pass
        else:
            igralec = self.zgodovina[-1][6]
            self.plosca[c][d] = nasprotnik(igralec)
            self.figurice[nasprotnik(igralec)] += 1
            self.mlin = True
            self.zgodovina[-1][4] = "PRAZNO"
            self.zgodovina[-1][5] = "PRAZNO"
            self.na_potezi = nasprotnik(self.na_potezi)

    def izpisi_plosco(self):  # to je funkcija namenjena programerju
        """ Izpise trenutno ploščo na lep način. Vsako vrstico posebej."""
        for vrstica in self.plosca:
            print(vrstica)

    def je_veljavna(self, i, j, a="PRAZNO", b="PRAZNO"):
        """Preveri, če je poteza veljavna. Poteza na (i,j) iz (a,b). """
        try:
            if self.faza == 0:
                return self.plosca[i][j] is None
            else:
                if self.plosca[i][j] is None and self.plosca[a][b] == self.na_potezi:
                    if self.figurice[self.na_potezi] == 3:
                        return True
                    else:
                        return (i, j) in self.sosedi[(a, b)]
                else:
                    return False
        except:
            return False

    def postavljen_mlin(self, poteza):
        """Glede na zadnjo potezo ugotovi ali je bil to potezo postavljen mlin. Vrne True ali False."""
        for trojka in self.kombinacije:  # poteza oblike (i,j)
            if poteza in trojka:
                trojica = []
                for polje in trojka:
                    trojica.append(self.plosca[polje[0]][polje[1]])
                if trojica == [IGRALEC_ENA, IGRALEC_ENA, IGRALEC_ENA] or trojica == [IGRALEC_DVA, IGRALEC_DVA,
                                                                                     IGRALEC_DVA]:
                    return True
        return False

    def veljavne_poteze(self):
        """ Glede na trenutno fazo vrne mogoče možne poteze. """
        mozne_poteze = []
        if self.faza == 0:
            for i in range(7):
                for j in range(7):
                    if self.je_veljavna(i, j, "PRAZNO", "PRAZNO"):
                        mozne_poteze.append((i, j, "PRAZNO", "PRAZNO"))
            return mozne_poteze
        elif self.faza == 1 and self.figurice[self.na_potezi] > 3:
            for i in range(7):
                for j in range(7):
                    if self.plosca[i][j] == self.na_potezi:
                        for sos in self.sosedi[(i, j)]:
                            if self.je_veljavna(sos[0], sos[1], i, j):
                                dod = (sos[0], sos[1], i, j)
                                mozne_poteze.append(dod)
            return mozne_poteze
        else:  # v primeru, da lahko letimo
            prosta_polja = []
            # poiscemo vsa prosta polja
            for i in range(7):
                for j in range(7):
                    if self.plosca[i][j] is None:
                        prosta_polja.append((i, j))
            # poiscemo vse 3 nase zetone in jih povezemo s prostimi polji
            for i in range(7):
                for j in range(7):
                    if self.plosca[i][j] == self.na_potezi:
                        for (prva, druga) in prosta_polja:
                            poteza = (prva, druga, i, j)
                            mozne_poteze.append(poteza)
            return mozne_poteze

    def veljavna_jemanja(self):
        """Funkcija vrne vse žetone, ki jih lahko pojemo. """
        lahko_vzamemo = []  # zetoni, ki jih lahko jemljemo
        vsi_naspr_zetoni = []  # vsi zetoni
        for i in range(7):
            for j in range(7):
                if self.plosca[i][j] == nasprotnik(self.na_potezi):
                    vsi_naspr_zetoni.append((i, j))
                    if self.postavljen_mlin((i, j)) is False:  # preverimo, ce je v mlinu
                        lahko_vzamemo.append((i, j))
        if len(lahko_vzamemo) == 0:  # če zetonov ni ali so vsi zetoni v mlinu,
            # lahko vzamemo karkoli. Situacija ko zetonov ni
            # je seveda trivialna in ni mogoča.
            return vsi_naspr_zetoni
        else:  # drugače vrnemo vse, ki jih lahko jemljemo!
            return lahko_vzamemo

    def lahko_jemljem(self, i, j):  # to bomo popravili na hitrejši način
        """Funkcija pove, ali izbrani zeton lahko pojemo."""
        return (i, j) in self.veljavna_jemanja()

    def poteza(self, i, j, a="PRAZNO", b="PRAZNO"):
        """Izvede potezo. kam (i,j) od kje (a,b). """
        if self.faza == 0:
            if self.je_veljavna(i, j):
                self.figurice[self.na_potezi] += 1
                self.postavljenih += 1
                if self.postavljenih >= 18:  # V primeru, da je konec faze postavljanja
                    self.faza = 1
                self.plosca[i][j] = self.na_potezi
                self.zgodovina.append([i, j, "PRAZNO", "PRAZNO", "PRAZNO", "PRAZNO", self.na_potezi])
                if self.postavljen_mlin((i, j)):
                    self.mlin = True
                else:
                    self.na_potezi = nasprotnik(self.na_potezi)
                    if len(self.veljavne_poteze()) == 0:
                        if self.na_potezi == IGRALEC_ENA:
                            self.stanje = ("ZMAGA", IGRALEC_DVA)
                        else:
                            self.stanje = ("ZMAGA", IGRALEC_ENA)
            else:
                self.izpisi_plosco()
                print("Poteza ni mogoča", self.na_potezi, i, j, self.faza)
        else:
            if self.plosca[a][b] == self.na_potezi:  # preveri da premikas svojo figurico
                if self.je_veljavna(i, j, a,
                                    b):  # preveri ali lahko tja premaknes svojo figurico (napisati je potrebno se da
                    # je mozno prestaviti figurico le na sosednja polja
                    self.plosca[a][b] = None
                    self.plosca[i][j] = self.na_potezi
                    self.zgodovina.append([i, j, a, b, "PRAZNO", "PRAZNO", self.na_potezi])
                    if self.postavljen_mlin((i, j)):
                        self.mlin = True
                    else:
                        self.na_potezi = nasprotnik(self.na_potezi)
                        if len(self.veljavne_poteze()) == 0:
                            if self.na_potezi == IGRALEC_ENA:
                                self.stanje = ("ZMAGA", IGRALEC_DVA)
                            else:
                                self.stanje = ("ZMAGA", IGRALEC_ENA)
                else:
                    print('Poteza iz ' + str((a, b)) + ' na polje ' + str((i, j)) + ' ni mogoča!')
            else:
                self.izpisi_plosco()
                print('tole pa ni tvoja figurica, Izberi svojo figuro', self.na_potezi, i, j, a, b, self.faza)

    def odstrani_figurico(self, i, j):
        """Odstrani nasprotnikovo figurico v primeru da jo je veljavno odstraniti."""
        if self.lahko_jemljem(i, j):
            polje = self.plosca[i][j]
            self.figurice[polje] -= 1
            self.plosca[i][j] = None
            self.zgodovina[-1][4] = i  # samo pripisemo zadnji potezi, kaj smo vzeli
            self.zgodovina[-1][5] = j
            self.na_potezi = nasprotnik(self.na_potezi)
            self.mlin = False
            if self.faza != 0:
                if self.figurice[self.na_potezi] < 3 or len(self.veljavne_poteze()) == 0:
                    if self.na_potezi == IGRALEC_ENA:
                        self.stanje = ("ZMAGA", IGRALEC_DVA)
                    else:
                        self.stanje = ("ZMAGA", IGRALEC_ENA)


class Igra_mcts_interface(Igra):
    def __init__(self, kopija, igralec):
        super(Igra_mcts_interface, self).__init__()

        self.trenutni_igralec = igralec
        self.plosca = kopija.plosca
        self.na_potezi = kopija.na_potezi
        self.faza = kopija.faza
        self.postavljenih = kopija.postavljenih
        self.figurice = kopija.figurice.copy()

    def getPossibleActions(self):
        poteze = self.veljavne_poteze()
        veljavne = list()
        for pot in poteze:
            self.je_veljavna(*pot)
            self.poteza(*pot)
            if self.mlin is True:
                jemanja = self.veljavna_jemanja()
                for jem in jemanja:
                    veljavne.append(pot + jem)
            else:
                veljavne.append(pot + ("PRAZNO", "PRAZNO"))
            self.razveljavi()
        return veljavne

    def takeAction(self, action):
        nova_poz = deepcopy(self)
        if len(action) == 6:
            pot,jem = action[:4],action[4:]
            nova_poz.poteza(*pot)
            nova_poz.odstrani_figurico(*jem)
        elif len(action) == 4:
            nova_poz.poteza(*action)
        return nova_poz

    def isTerminal(self):
        return self.stanje[0] == "ZMAGA"

    def getReward(self):
        if self.trenutni_igralec == self.stanje[1]:
            return 10
        else:
            return 0

    def __eq__(self, other):
        return self.plosca == other.plosca and self.faza == other.faza and self.na_potezi == other.na_potezi

