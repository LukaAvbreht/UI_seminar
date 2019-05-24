from igra import *
import random

from mcts import mcts


class MiniMax:
    """Vrne tri argumente (kam, od kje),(kaj jemljemo),vrednost poteze v obliki poteze"""

    def __init__(self, globina, hevristika):
        self.globina = int(globina)
        self.igra = None
        self.jaz = None
        self.poteza = None  # sem algoritem shrani potezo ko jo naredi
        self.jemljem = None
        self.hevristika = hevristika

    ZMAGA = 1000000  # Mora biti vsaj 10^6
    NESKONCNO = ZMAGA + 1  # Več kot zmaga

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.jaz = self.igra.na_potezi
        self.poteza = None
        self.jemljem = None
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.igra = None
        self.jaz = None
        self.poteza = poteza[:4]
        self.jemljem = poteza[4:]

    def vrednost_pozicije(self):
        """Vrne oceno vrednosti pozicije."""
        return self.hevristika(self, self.jaz) - self.hevristika(self, nasprotnik(self.jaz))

    def minimax(self, globina, maksimiziramo):
        (stanje, kdo) = self.igra.stanje
        if stanje == "ZMAGA":
            if kdo == self.jaz:
                return (None, self.ZMAGA)
            elif kdo == nasprotnik(self.jaz):
                return (None, - self.ZMAGA)
            else:
                pass
        elif stanje == "V TEKU":
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                if maksimiziramo:
                    najboljsa_poteza = None  # (i,j,a,b,c,d)
                    vrednost_najboljse = - MiniMax.NESKONCNO
                    poteze = self.igra.veljavne_poteze()
                    random.shuffle(poteze)
                    for p in poteze:
                        if self.igra.je_veljavna(p[0], p[1], p[2], p[3]):
                            self.igra.poteza(p[0], p[1], p[2], p[3])
                            if self.igra.mlin is True:
                                for q in self.igra.veljavna_jemanja():
                                    self.igra.odstrani_figurico(q[0], q[1])
                                    vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                                    self.igra.razveljavi_jemanje()
                                    if vrednost > vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljsa_poteza = p + q  # sestevanje tuplov
                                self.igra.mlin = False
                                self.igra.razveljavi()
                            else:
                                vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                                self.igra.razveljavi()
                                if vrednost > vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p + ("PRAZNO", "PRAZNO")
                        else:
                            pass
                else:  # minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = MiniMax.NESKONCNO
                    poteze = self.igra.veljavne_poteze()
                    random.shuffle(poteze)
                    for p in poteze:
                        if self.igra.je_veljavna(p[0], p[1], p[2], p[3]):
                            self.igra.poteza(p[0], p[1], p[2], p[3])
                            if self.igra.mlin == True:
                                for q in self.igra.veljavna_jemanja():
                                    self.igra.odstrani_figurico(q[0], q[1])
                                    vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                                    self.igra.razveljavi_jemanje()
                                    if vrednost < vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljsa_poteza = p + q
                                self.igra.mlin = False
                                self.igra.razveljavi()
                            else:
                                vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                                self.igra.razveljavi()
                                if vrednost < vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p + ("PRAZNO", "PRAZNO")
                        else:
                            pass

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return najboljsa_poteza, vrednost_najboljse


class AlphaBetta:
    """Vrne tri argumente (kam, od kje),(kaj jemljemo),vrednost poteze v obliki poteze"""

    def __init__(self, globina, hevristika):
        self.globina = int(globina)
        self.igra = None
        self.jaz = None
        self.poteza = None  # sem algoritem shrani potezo ko jo naredi
        self.jemljem = None
        self.hevristika = hevristika

    ZMAGA = 1000000  # Mora biti vsaj 10^6
    NESKONCNO = ZMAGA + 1  # Več kot zmaga

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.jaz = self.igra.na_potezi
        self.poteza = None
        self.jemljem = None
        (poteza, vrednost) = self.alfabeta(self.globina, -100001, 100001, True)
        self.igra = None
        self.jaz = None
        self.poteza = poteza[:4]
        self.jemljem = poteza[4:]

    def vrednost_pozicije(self):
        """Vrne oceno vrednosti pozicije."""
        return self.hevristika(self, self.jaz) - self.hevristika(self, nasprotnik(self.jaz))

    def alfabeta(self, globina, alfa, beta, maksimiziramo):
        novaalfa = alfa
        novabeta = beta
        (stanje, kdo) = self.igra.stanje
        if stanje == "ZMAGA":
            if kdo == self.jaz:
                return (None, self.ZMAGA)
            elif kdo == nasprotnik(self.jaz):
                return (None, - self.ZMAGA)
            else:
                pass
        elif stanje == "V TEKU":
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                if maksimiziramo:
                    najboljsa_poteza = None  # (i,j,a,b,c,d)
                    vrednost_najboljse = - AlphaBetta.NESKONCNO
                    poteze = self.igra.veljavne_poteze()
                    random.shuffle(poteze)
                    for p in poteze:
                        FLAG = False
                        if self.igra.je_veljavna(p[0], p[1], p[2], p[3]):
                            self.igra.poteza(p[0], p[1], p[2], p[3])
                            if self.igra.mlin == True:
                                for q in self.igra.veljavna_jemanja():
                                    self.igra.odstrani_figurico(q[0], q[1])
                                    vrednost = self.alfabeta(globina - 1, novaalfa, novabeta, not maksimiziramo)[1]
                                    self.igra.razveljavi_jemanje()
                                    if vrednost > vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljsa_poteza = p + q  # sestevanje tuplov
                                        novaalfa = max(novaalfa, vrednost_najboljse)
                                        if novaalfa >= novabeta:
                                            FLAG = True
                                            break
                                self.igra.mlin = False
                                self.igra.razveljavi()
                            else:
                                vrednost = self.alfabeta(globina - 1, novaalfa, novabeta, not maksimiziramo)[1]
                                self.igra.razveljavi()
                                if vrednost > vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p + ("PRAZNO", "PRAZNO")
                                    novaalfa = max(novaalfa, vrednost_najboljse)
                                    if novaalfa >= novabeta:
                                        break
                            if FLAG:
                                break
                        else:
                            pass
                else:  # minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = AlphaBetta.NESKONCNO
                    poteze = self.igra.veljavne_poteze()
                    random.shuffle(poteze)
                    for p in poteze:
                        FLAG = False
                        if self.igra.je_veljavna(p[0], p[1], p[2], p[3]):
                            self.igra.poteza(p[0], p[1], p[2], p[3])
                            if self.igra.mlin is True:
                                for q in self.igra.veljavna_jemanja():
                                    self.igra.odstrani_figurico(q[0], q[1])
                                    vrednost = self.alfabeta(globina - 1, novaalfa, novabeta, not maksimiziramo)[1]
                                    self.igra.razveljavi_jemanje()
                                    if vrednost < vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljsa_poteza = p + q
                                        novabeta = min(novabeta, vrednost_najboljse)
                                        if novabeta <= novaalfa:
                                            FLAG = True
                                            break
                                self.igra.mlin = False
                                self.igra.razveljavi()
                            else:
                                vrednost = self.alfabeta(globina - 1, novaalfa, novabeta, not maksimiziramo)[1]
                                self.igra.razveljavi()
                                if vrednost < vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p + ("PRAZNO", "PRAZNO")
                                    novabeta = min(novabeta, vrednost_najboljse)
                                    if novabeta <= novaalfa:
                                        break
                            if FLAG:
                                break
                        else:
                            pass
                assert (najboljsa_poteza is not None), "alfabeta: izračunana poteza je None"
                return najboljsa_poteza, vrednost_najboljse


class PureMonteCarloTreeSearch:
    def __init__(self, timeLimit=None, iterationLimit=None):
        self.igra = None
        self.jaz = None
        self.poteza = None  # sem algoritem shrani potezo ko jo naredi
        self.jemljem = None
        self.mcts_timeLimit = timeLimit
        self.mcts_iterationLimit = iterationLimit

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.jaz = self.igra.na_potezi
        self.poteza = None
        self.jemljem = None
        poteza = self.pure_mcts()
        print(poteza)
        self.igra = None
        self.jaz = None
        self.poteza = poteza[:4]
        self.jemljem = poteza[4:]

    def pure_mcts(self):
        initialState = Igra_mcts_interface(self.igra, self.jaz)
        MCTS = mcts(timeLimit=self.mcts_timeLimit, iterationLimit=self.mcts_iterationLimit)
        action = MCTS.search(initialState=initialState)
        return action
