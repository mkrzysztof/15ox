"""zawiera potrzebne klasy"""
import collections
import operator
import math
import enum


StanGry = collections.namedtuple("StanGry", "siatka ostatni_ruch")

class Faza(enum.Enum):
    """reprezentuje fazę w algorytmie alfa-beta"""
    ALFA = enum.auto()
    BETA = enum.auto()

_PRZECIWNE = {Faza.ALFA: Faza.BETA, Faza.BETA: Faza.ALFA}
def przeciwna(faza):
    """faza przeciwna do fazy f"""
    return _PRZECIWNE[faza]

_MNOZNIKI = {Faza.ALFA: 1, Faza.BETA: -1}
def mnoznik(faza):
    """z jakim znakiem przyznawane są punkty za sytuację na planszy"""
    return _MNOZNIKI[faza]


# ocena potrzebna do zdecydowania o ruchu
Ocena = collections.namedtuple("Ocena", "ruch wartosc")


def nowe_ograniczenia():
    """stwarza nowe początkowe ograniczenia alfa = -inf, beta = +inf"""
    ocena_alfa = Ocena(None, -math.inf)
    ocena_beta = Ocena(None, math.inf)
    return Ograniczenia(ocena_alfa, ocena_beta)

class Ograniczenia:
    """dolne i górne ograniczenie w algorytmie alfa-beta"""
    def __init__(self, ocena_alfa=None, ocena_beta=None):
        self._ograniczenia = {Faza.ALFA: ocena_alfa, Faza.BETA: ocena_beta}

    def pobierz(self, faza):
        """pobiera ograniczenie typu Ocena dla fazy f"""
        return self._ograniczenia[faza]

    def aktualizuj(self, faza, ocena, ruch):
        """aktualizuj obiekt dla fazy f na podstawie oceny n i ruchu ruch"""
        nowe_ocena = Ocena(ruch=ruch, wartosc=ocena.wartosc)
        self._ograniczenia[faza] = nowe_ocena

    def czy_ciecie(self):
        """czy należy przerwać przeszukiwanie alfa >= beta"""
        ogr_alfa = self.pobierz(Faza.ALFA)
        ogr_beta = self.pobierz(Faza.BETA)
        return ogr_alfa.wartosc >= ogr_beta.wartosc

    _aktual_tab = {Faza.ALFA: operator.gt, Faza.BETA: operator.lt}
    def czy_aktualizowac(self, faza, ocena):
        """czy na podstawie oceny n zaktualizować obiekt dla fazy f"""
        ocena_f = self.pobierz(faza)
        return self._aktual_tab[faza](ocena.wartosc, ocena_f.wartosc)

    def warunkowo_aktualizuj(self, faza, ocena, stan_gry):
        """aktualizacja obiektu, gdy zachodzi taka potrzeba
        f -- faza w której aktualizujemy
        ocena
        stan_gry -- stan_gry który w danej chwili jest rozpatrywany"""
        if self.czy_aktualizowac(faza, ocena):
            self.aktualizuj(faza, ocena, stan_gry.ostatni_ruch)

    def copy(self):
        """kopiowanie"""
        ogr_copy = Ograniczenia()
        for k in self._ograniczenia.keys():
            ogr_copy._ograniczenia[k] = self._ograniczenia[k]
        return ogr_copy
