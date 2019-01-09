"""zawiera potrzebne klasy"""
import collections
import math
import copy
import enum

StanGry = collections.namedtuple("StanGry", "siatka ostatni_ruch")

class Faza(enum.Enum):
    """reprezentuje fazę w algorytmie alfa-beta"""
    ALFA = enum.auto()
    BETA = enum.auto()

def przeciwna(f):
    """faza przeciwna do fazy f"""
    assert f in {Faza.ALFA, Faza.BETA}
    if f == Faza.ALFA:
        return Faza.BETA
    return Faza.ALFA

def mnoznik(f):
    """z jakim znakiem przyznawane są punkty za sytuację na planszy"""
    if f == Faza.ALFA:
        return 1
    else:
        return -1

class Gracze:
    """trzyma w sobie graczy biorących udział w rozgrywce"""
    def __init__(self, gracz_alfa, gracz_beta):
        """przypisanie graczy do poszczególnych faz"""
        self._gracze = {Faza.ALFA: gracz_alfa, Faza.BETA: gracz_beta}

    def gracz_w_fazie(self, f):
        """gracz przypisany do fazy f"""
        return self._gracze[f]

class Ocena:
    """ocena potrzebna do zdecydowania o ruchu"""
    def __init__(self, ruch, wartosc):
        """ inicjalizuje self
        ruch to siatka.Polozenie
        wartosc to wartość liczbowa po wykonaniu ruchu ruch """
        self._ruch = ruch
        self._wartosc = wartosc

    def wymien_ruch(self, ruch):
        self._ruch = ruch

    def pokaz_ruch(self):
        return self._ruch
        
    def wieksza(self, n):
        """self > n po wartościach"""
        return self._wartosc > n._wartosc

    def wieksza_rowna(self, n):
        return self._wartosc >= n._wartosc

    def mniejsza(self, n):
        """self < n po wartościach"""
        return self._wartosc < n._wartosc

    def copy(self):
        """kopiuje obiekt"""
        return Ocena(self._ruch, self._wartosc)

    def __eq__(self, value):
        return self._ruch == value._ruch and self._wartosc == value._wartosc

    def __repr__(self):
        lista_nap = ["(", repr(self._ruch), ", ", repr(self._wartosc), ")"]
        return "".join(lista_nap)
        

def nowe_ograniczenia():
    """stwarza nowe początkowe ograniczenia alfa = -inf, beta = +inf"""
    ocena_alfa = Ocena(None, -math.inf)
    ocena_beta = Ocena(None, math.inf)
    return Ograniczenia(ocena_alfa, ocena_beta)

class Ograniczenia:
    """dolne i górne ograniczenie w algorytmie alfa-beta"""
    def __init__(self, ocena_alfa=None, ocena_beta=None):
        self._ograniczenia = {Faza.ALFA: ocena_alfa, Faza.BETA: ocena_beta}


    def pobierz(self, f):
        """pobiera ograniczenie typu Ocena dla fazy f"""
        return self._ograniczenia[f]
    
    def aktualizuj(self, f, n, ruch):
        """aktualizuj obiekt dla fazy f na podstawie oceny n i ruchu ruch"""
        nowe_n = copy.copy(n)
        nowe_n.wymien_ruch(ruch)
        self._ograniczenia[f] = nowe_n
    
    def czy_ciecie(self):
        """czy należy przerwać przeszukiwanie alfa >= beta"""
        ogr_alfa = self.pobierz(Faza.ALFA)
        ogr_beta = self.pobierz(Faza.BETA)
        return ogr_alfa.wieksza_rowna(ogr_beta)

    def czy_aktualizowac(self, f, n):
        """czy na podstawie oceny n zaktualizować obiekt dla fazy f"""
        ocena_f = self.pobierz(f)
        if f == Faza.ALFA:
            return n.wieksza(ocena_f)
        else:
            return n.mniejsza(ocena_f)

    def warunkowo_aktualizuj(self, f, n, stan_gry):
        """aktualizacja obiektu, gdy zachodzi taka potrzeba
        f -- faza w której aktualizujemy
        n -- ocena
        stan_gry -- stan_gry który w danej chwili jest rozpatrywany"""
        if self.czy_aktualizowac(f, n):
            self.aktualizuj(f, n, stan_gry.ostatni_ruch)

    def copy(self):
        ogr_copy = Ograniczenia()
        for k in self._ograniczenia.keys():
            ogr_copy._ograniczenia[k] = self._ograniczenia[k]
        return ogr_copy