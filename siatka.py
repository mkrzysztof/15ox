""" Moduł zawiera fefinicję klas Polozenie i Siatka"""

#stałe
WIERSZ = 0
KOLUMNA = 1
WYGRYWAJACYCH = 3

POZIOM = "poziom"
PION = "pion"
UKOS_LEWY = "ukos_lewy"
UKOS_PRAWY = "ukos_prawy"

LEWO = (0, -1)
PRAWO = (0, 1)
GORA = (-1, 0)
DOL = (1, 0)

def _dodaj_tuple(tuple1, tuple2):
    return (tuple1[WIERSZ] + tuple2[WIERSZ], tuple1[KOLUMNA] + tuple2[KOLUMNA])

LEWO_GORA = _dodaj_tuple(LEWO, GORA)
LEWO_DOL = _dodaj_tuple(LEWO, DOL)
PRAWO_GORA = _dodaj_tuple(PRAWO, GORA)
PRAWO_DOL = _dodaj_tuple(PRAWO, DOL)

KIERUNKI = (LEWO, PRAWO, GORA, DOL, LEWO_GORA, LEWO_DOL, PRAWO_GORA, PRAWO_DOL)

class Polozenie(tuple):
    """reprezentuje położenie"""

    def przesun(self, translacja):
        return Polozenie(_dodaj_tuple(self, translacja))


class Siatka:
    """reprezentuje siatkę na której gracze stawiają symbole"""

    def __repr_wiersz(self, num_wiersz):
        wyj = []
        for num_kol in range(self.kolumn):
            symbol = self[Polozenie((num_wiersz, num_kol))]
            if symbol:
                wyj.append(symbol.repr)
            else:
                wyj.append(".")
        return wyj

    def _inicjuj_wolne_pola(self):
        if not self._wolne_pola:
            self._wolne_pola = set(Polozenie((x, y))
                                   for x in range(self.wierszy)
                                   for y in range(self.kolumn))

    def __init__(self, wierszy=15, kolumn=15):
        self.pola = [[None] * kolumn for y in range(wierszy)]
        self.wierszy = wierszy
        self.kolumn = kolumn
        self._wolne_pola = None
        self._otoczenie = set()

    def __getitem__(self, polozenie):
        return self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]]

    def __setitem__(self, polozenie, symbol_gracza):
        self._inicjuj_wolne_pola()
        self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]] = symbol_gracza
        self._wolne_pola.discard(polozenie)
        self.zaktualizuj_otoczenie(polozenie)

    def __repr__(self):
        bufor = []
        for num_wiersza in range(self.wierszy):
            bufor.extend(self.__repr_wiersz(num_wiersza))
            bufor.append("\n")
        return "".join(bufor)

    def _nalezy_do_wolnych(self, x):
        return x in self._wolne_pola

    def zaktualizuj_otoczenie(self, polozenie):
        """aktualizuje _otoczenie wszystkich punktów siatki po dodaniu
        symbolu na pozycji polozenie"""
        kandydat_otoczenie = {Polozenie(_dodaj_tuple(polozenie, kierunek))
                           for kierunek in KIERUNKI}
        otocz_polozenie = filter(self.zawiera_polozenie, kandydat_otoczenie)
        self._otoczenie.discard(polozenie)
        otocz_polozenie = filter(self._nalezy_do_wolnych, otocz_polozenie)
        self._otoczenie.update(otocz_polozenie)

    def zawiera_polozenie(self, polozenie):
        return (0 <= polozenie[WIERSZ] < self.wierszy
                and 0 <= polozenie[KOLUMNA] < self.kolumn)

    def copy(self):
        wyjscie = Siatka(self.wierszy, self.kolumn)
        for numer, wiersz in enumerate(self.pola):
            wyjscie.pola[numer] = wiersz[:]
        self._inicjuj_wolne_pola()
        wyjscie._wolne_pola = self._wolne_pola.copy()
        wyjscie._otoczenie = set(self._otoczenie)
        return wyjscie

    def kasuj_wolne_pola(self):
        """ ustawia zbiór wolnych pól na pusty """
        self._wolne_pola = set()

    def jest_zapelniona(self):
        """sprawdza czy plansza jest całkowicie wypełniona"""
        return not self._wolne_pola

    def policz_symbol(self, symbol_gracza, polozenie, translacja):
        licznik = 0
        while self.zawiera_polozenie(polozenie):
            if self[polozenie] != symbol_gracza:
                break
            licznik += 1
            polozenie = polozenie.przesun(translacja)
        return licznik

    _strony = {"poziom": (PRAWO, LEWO),
               "pion": (DOL, GORA),
               "ukos_lewy": (PRAWO_DOL, LEWO_GORA),
               "ukos_prawy": (LEWO_DOL, PRAWO_GORA),}

    def policz_symbol_strona(self, polozenie, strona):
        """ policz ciągłe wystąpienia symbolu wokół położenia dla
        strony """
        licznik = 0
        symbol_sprawdzany = self[polozenie]
        translacja1, translacja2 = self._strony[strona]
        licznik = self.policz_symbol(symbol_sprawdzany, polozenie, translacja1)
        polozenie = polozenie.przesun(translacja2)
        licznik += self.policz_symbol(symbol_sprawdzany, polozenie,
                                      translacja2)
        return licznik

    def wygrywa_strona(self, polozenie, strona):
        return self.policz_symbol_strona(polozenie, strona) >= WYGRYWAJACYCH

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        wyj = False
        if polozenie is None:
            return wyj
        for strona in self._strony:
            if self.wygrywa_strona(polozenie, strona):
                wyj = True
                break
        return wyj

    def wolne_pola(self):
        self._inicjuj_wolne_pola()
        return self._wolne_pola

    def otoczenie(self):
        return self._otoczenie

def wolne_pola(siatka1):
    return siatka1.wolne_pola()

def otoczenie(siatka1):
    return siatka1.otoczenie()
