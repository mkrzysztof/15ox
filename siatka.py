""" Moduł zawiera fefinicję klas Polozenie i Siatka"""
import enum
import itertools
import symbol

#stałe
WIERSZ = 0
KOLUMNA = 1
WYGRYWAJACYCH = 3

def _dodaj_tuple(t1, t2):
    return (t1[WIERSZ] + t2[WIERSZ], t1[KOLUMNA] + t2[KOLUMNA])

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
    wszystkie = None
    def __init__(self, wierszy=15, kolumn=15):
        self.pola = [[symbol.Puste] * kolumn for y in range(wierszy)]
        self.wierszy = wierszy
        self.kolumn = kolumn
        if self.__class__.wszystkie is None:
            self.__class__.wszystkie = list(
                itertools.product(range(self.wierszy), range(self.kolumn)))

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

    def czy_polozenie_puste(self, polozenie):
        return self[polozenie] == symbol.Puste

    def copy(self):
        """kopia ale tylko pola pola"""
        wyjscie = Siatka(self.wierszy, self.kolumn)
        for numer, wiersz in enumerate(self.pola):
            wyjscie.pola[numer] = wiersz[:]
        return wyjscie

    def __getitem__(self, polozenie):
        return self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]]

    def __setitem__(self, polozenie, symbol_gracza):
        self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]] = symbol_gracza

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
        zap = True
        for wiersz in self.pola:
            zap = zap and (Siatka._wiersz_jest_zapelniony(wiersz))
            if not zap:
                break
        return zap

    def __ma_uklad_wygrywajacy_w_kierunkach(self, polozenie,
                                            kierunki):
        symbol_sprawdzany = self[polozenie]
        #kierunek1
        licznik = self.__zliczaj_symbole_w_kierunku(symbol_sprawdzany,
                                                     polozenie,
                                                     kierunki[0])
        #kierunek2
        polozenie = polozenie.przesun(kierunki[1])
        licznik += self.__zliczaj_symbole_w_kierunku(symbol_sprawdzany,
                                                     polozenie,
                                                     kierunki[1])
        return licznik >= WYGRYWAJACYCH

    __strony = ((Translacja.PRAWO, Translacja.LEWO), #poziom
                (Translacja.DOL, Translacja.GORA), #pion
                (Translacja.PRAWO_DOL, Translacja.LEWO_GORA), #ukos_lewy
                (Translacja.LEWO_DOL, Translacja.PRAWO_GORA) #ukos_prawy
               )

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        wyj = False
        for kierunek in Siatka.__strony:
            if self.__ma_uklad_wygrywajacy_w_kierunkach(polozenie, kierunek):
                wyj = True
                break
        return wyj

    def wolne_pola(self):
        """ zwraca generator wolnych pól (Polozenie) siatki """        
        # for para in wszystkie:
        #     ruch = Polozenie(para)
        #     if self.czy_polozenie_puste(ruch):
        #         yield ruch
        return filter(self.czy_polozenie_puste,
                      map(Polozenie, self.__class__.wszystkie))

    def __zliczaj_symbole_w_kierunku(self, symbol_gracza, polozenie,
                                     translacja):
        licznik = 0
        while self.zawiera_polozenie(polozenie):
            if self[polozenie] != symbol_gracza:
                break
            licznik += 1
            polozenie = polozenie.przesun(translacja)
        return licznik

    __slownik = {'x': symbol.Krzyzyk, 'o': symbol.Kolko, '.': symbol.Puste}
    def _wczytaj_linie_na_wiersz(self, linia, numer_wiersza):
        bufor = []
        slownik = Siatka.__slownik
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
