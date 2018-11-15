""" Moduł zawiera fefinicję klas Polozenie i Siatka"""
import enum
import symbol

#stałe
WIERSZ = 0
KOLUMNA = 1
WYGRYWAJACYCH = 3

def _dodaj_tuple(tuple1, tuple2):
    return (tuple1[WIERSZ] + tuple2[WIERSZ], tuple1[KOLUMNA] + tuple2[KOLUMNA])

class Translacja(enum.Enum):
    """określa przesunięcia w 8-miu możliwych kierunkach"""
    LEWO = (0, -1)
    PRAWO = (0, 1)
    GORA = (-1, 0)
    DOL = (1, 0)
    LEWO_GORA = _dodaj_tuple(LEWO, GORA)
    LEWO_DOL = _dodaj_tuple(LEWO, DOL)
    PRAWO_GORA = _dodaj_tuple(PRAWO, GORA)
    PRAWO_DOL = _dodaj_tuple(PRAWO, DOL)


class Polozenie(tuple):
    """reprezentuje położenie"""

    def przesun(self, translacja):
        return Polozenie(_dodaj_tuple(self, translacja.value))


class Siatka:
    """reprezentuje siatkę na której gracze stawiają symbole"""
    def __init__(self, wierszy=15, kolumn=15):
        self.pola = [[symbol.Puste] * kolumn for y in range(wierszy)]
        self.wierszy = wierszy
        self.kolumn = kolumn
        self._wolne_pola = None

    def __repr_wiersz(self, num_wiersz):
        return [self[Polozenie((num_wiersz, num_kol))].repr
                for num_kol in range(self.kolumn)]

    def __repr__(self):
        bufor = []
        for num_wiersza in range(self.wierszy):
            bufor.extend(self.__repr_wiersz(num_wiersza))
            bufor.append("\n")
        return "".join(bufor)

    def zawiera_polozenie(self, polozenie):
        return (0 <= polozenie[WIERSZ] < self.wierszy
                and 0 <= polozenie[KOLUMNA] < self.kolumn)

    def copy(self):
        """kopia ale tylko pola pola"""
        wyjscie = Siatka(self.wierszy, self.kolumn)
        for numer, wiersz in enumerate(self.pola):
            wyjscie.pola[numer] = wiersz[:]
        self.inicjuj_wolne_pola()
        wyjscie._wolne_pola = self._wolne_pola.copy()
        return wyjscie

    def inicjuj_wolne_pola(self):
        if self._wolne_pola is None:
            self._wolne_pola = set(Polozenie((x, y))
                                   for x in range(self.wierszy)
                                   for y in range(self.kolumn))

    def kasuj_wolne_pola(self):
        """ ustawia zbiór wolnych pól na pusty """
        self._wolne_pola = set()

    def __getitem__(self, polozenie):
        return self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]]

    def __setitem__(self, polozenie, symbol_gracza):
        self.inicjuj_wolne_pola()
        self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]] = symbol_gracza
        self._wolne_pola.discard(polozenie)

    def jest_zapelniona(self):
        """sprawdza czy plansza jest całkowicie wypełniona"""
        return not self._wolne_pola

    def __ma_uklad_wygrywajacy_w_kierunkach(self, polozenie, kierunki):
        symbol_sprawdzany = self[polozenie]
        licznik = self.__zliczaj_symbole_w_kierunku(symbol_sprawdzany,
                                                    polozenie,
                                                    kierunki[0])
        polozenie = polozenie.przesun(kierunki[1])
        licznik += self.__zliczaj_symbole_w_kierunku(symbol_sprawdzany,
                                                     polozenie,
                                                     kierunki[1])
        return licznik >= WYGRYWAJACYCH

    _strony = ((Translacja.PRAWO, Translacja.LEWO), #poziom
                (Translacja.DOL, Translacja.GORA), #pion
                (Translacja.PRAWO_DOL, Translacja.LEWO_GORA), #ukos_lewy
                (Translacja.LEWO_DOL, Translacja.PRAWO_GORA) #ukos_prawy
               )

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        wyj = False
        if polozenie is None:
            return wyj
        for kierunek in self._strony:
            if self.__ma_uklad_wygrywajacy_w_kierunkach(polozenie, kierunek):
                wyj = True
                break
        return wyj

    def wolne_pola(self):
        self.inicjuj_wolne_pola()
        return self._wolne_pola

    def __zliczaj_symbole_w_kierunku(self, symbol_gracza, polozenie,
                                     translacja):
        licznik = 0
        while self.zawiera_polozenie(polozenie):
            if self[polozenie] != symbol_gracza:
                break
            licznik += 1
            polozenie = polozenie.przesun(translacja)
        return licznik

    _slownik = {'x': symbol.Krzyzyk, 'o': symbol.Kolko, '.': symbol.Puste}
    def _wczytaj_linie_na_wiersz(self, linia, numer_wiersza):
        bufor = []
        for sym in linia:
            bufor.append(self._slownik[sym])
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
