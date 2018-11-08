""" Moduł zawiera fefinicję klas Polozenie i Siatka"""
import itertools
import symbol
import enum
import pygame

WYGRYWAJACYCH = 3

class Translacja(enum.Enum):
    LEWO  = (0, -1)
    PRAWO = (0, 1)
    GORA  = (-1, 0)
    DOL   = (1, 0)
    LEWO_GORA = (-1, -1)
    LEWO_DOL = (1, -1)
    PRAWO_GORA = (-1, 1)
    PRAWO_DOL = (1, 1)

class Strona(enum.Enum):
    POZIOM = (Translacja.PRAWO, Translacja.LEWO)
    PION   = (Translacja.DOL, Translacja.GORA)
    LEWO   = (Translacja.PRAWO_DOL, Translacja.LEWO_GORA)
    PRAWO  = (Translacja.LEWO_DOL, Translacja.PRAWO_GORA)

class Polozenie(object):
    """reprezentuje położenie (wiersz, kolumna) """

    __slots__ = ['poz']

    def __init__(self, wiersz, kolumna):
        self.poz = (wiersz, kolumna)

    def __hash__(self):
        return hash(self.poz)

    def __eq__(self, other):
        return self.poz == other.poz

    def __add__(self, przesuniecie):
        # przesuniecie to (x,y)
        tr_wiersz, tr_kolumna = przesuniecie
        wiersz, kolumna = self
        return Polozenie(wiersz + tr_wiersz, kolumna + tr_kolumna)

    def __getitem__(self, key):
        return self.poz[key]

_wszystkie = None
class Siatka:
    """reprezentuje siatkę na której gracze stawiają symbole"""
    def __init__(self, wierszy=15, kolumn=15):
        global _wszystkie
        self.pola = {}
        self.zb_kluczy = set()
        self.rozmiar = (wierszy, kolumn)
        self._rect = pygame.Rect((0, 0), self.rozmiar) 
        self._liczba_pol = kolumn * wierszy
        if _wszystkie is None:
            _wszystkie = list(itertools.product(range(self.rozmiar[0]),
                                            range(self.rozmiar[1])))

    def __repr_wiersz(self, num_wiersz):
        _, kolumn = self.rozmiar
        return [self[Polozenie(num_wiersz, num_kol)].repr
                for num_kol in range(kolumn)]

    def __repr__(self):
        bufor = []
        wierszy, _ = self.rozmiar
        for num_wiersza in range(wierszy):
            bufor.extend(self.__repr_wiersz(num_wiersza))
            bufor.append("\n")
        return "".join(bufor)

    def zawiera_polozenie(self, polozenie):
        """czy dane położenie znajduje się na siatce czy poza nią"""
        wiersz, kolumna = polozenie
        l_wierszy, l_kolumn = self.rozmiar
        return (wiersz * (l_wierszy - 1 - wiersz) >= 0
                and kolumna * (l_kolumn - 1 - kolumna) >= 0)
        # return 0 <= wiersz < l_wierszy and 0 <= kolumna < l_kolumn

    def _wczytaj_linie_na_wiersz(self, linia, numer_wiersza):
        bufor = []
        slownik = {'x': symbol.Krzyzyk, 'o': symbol.Kolko, '.': symbol.Puste}
        for sym in linia:
            bufor.append(slownik[sym])
        self.pola[numer_wiersza] = bufor

    def wypelnij_siatke(self, wzor):
        """ wypełnij siatkę podanym wzorem:
        [
         'xo.xo.',
         'o...x.',
            .
            .
         'xxxxo.',
        ]
        gdzie kropka oznacza puste miejsce, wzór powinien być tak dobrany
        by pasował do rozmiarów siatki
        """
        for numer, linia in enumerate(wzor):
            self._wczytaj_linie_na_wiersz(linia, numer)

    def copy(self):
        """kopia ale tylko pola pola"""
        wierszy, kolumn = self.rozmiar
        wyjscie = Siatka(wierszy, kolumn)
        wyjscie.pola = self.pola.copy()
        return wyjscie

    def __getitem__(self, polozenie):
        # try:
        #     wyj = self.pola[polozenie]
        # except KeyError:
        #     wyj = symbol.Puste
        pola = self.pola
        wyj = symbol.Puste
        if polozenie in self.zb_kluczy:
            wyj = pola[polozenie]
        return wyj

    def __setitem__(self, polozenie, symbol_gracza):
        self.pola[polozenie] = symbol_gracza
        self.zb_kluczy.add(polozenie)

    def __zajeta(self, polozenie):
        odczytany_symbol = self[polozenie]
        return odczytany_symbol != symbol.Puste

    @staticmethod
    def _wiersz_jest_zapelniony(wiersz):
        zap = True
        for badany_symbol in wiersz:
            zap = zap and (badany_symbol != symbol.Puste)
            if not zap:
                break
        return zap

    def jest_zapelniona(self):
        """sprawdza czy plansza jest całkowicie wypełniona"""
        pola = self.pola
        ile_zapelnionych = 0
        # policz zapełnione pola
        for pole in pola:
            ile_zapelnionych += 1
        return ile_zapelnionych == self._liczba_pol

    def __ma_uklad_wygrywajacy_dla_strony(self, arg_polozenie, strona):
        polozenie = arg_polozenie
        symbol_sprawdzany = self[polozenie]
        fun_zliczaj = self.__zliczaj_symbole_w_kierunku
        strona0, strona1 = strona
        licznik = 0
        #kierunek1
        licznik += fun_zliczaj(symbol_sprawdzany, polozenie, strona0)
        #kierunek2
        polozenie = polozenie + strona1.value
        licznik += fun_zliczaj(symbol_sprawdzany, polozenie, strona1)
        return licznik >= WYGRYWAJACYCH

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        wyj = False
        for strona in Strona:
            if self.__ma_uklad_wygrywajacy_dla_strony(polozenie, strona.value):
                wyj = True
                break
        return wyj

    def wolne_pola(self):
        """ zwraca generator wolnych pól (Polozenie) siatki """
        wszystkie = _wszystkie
        for para in wszystkie:
            ruch = Polozenie(*para)
            if not self.__zajeta(ruch):
                yield ruch

    def __zliczaj_symbole_w_kierunku(self, symbol_gracza, arg_polozenie,
                                     translacja):
        licznik = 0
        polozenie = arg_polozenie
        while self.zawiera_polozenie(polozenie):
            if self[polozenie] == symbol_gracza:
                licznik += 1
                polozenie = polozenie + translacja.value
            else:
                break
        return licznik
