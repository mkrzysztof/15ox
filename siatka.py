""" Moduł zawiera fefinicję klas Polozenie i Siatka"""
import itertools
import symbol
import enum

#stałe
#WIERSZ = 0
#KOLUMNA = 1
WYGRYWAJACYCH = 3

class Kierunek(enum.Enum):
    LEWO  = (0, -1)
    PRAWO = (0, 1)
    GORA  = (-1, 0)
    DOL   = (1, 0)
    LEWO_GORA = (-1, -1)
    LEWO_DOL = (1, -1)
    PRAWO_GORA = (-1, 1)
    PRAWO_DOL = (1, 1)

class Polozenie(object):
    """reprezentuje położenie (wiersz, kolumna) """

    __slots__ = ['poz']
    x = 1

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

    def w_lewo(self):
        """zwraca nowe położenie przesunięte w lewo"""
        return self + Kierunek.LEWO.value

    def w_prawo(self):
        """zwraca nowe położenie przesunięte w prawo"""
        return self + Kierunek.PRAWO.value
    
    def w_gore(self):
        """zwraca nowe położenie przesunięte w górę"""
        return self + Kierunek.GORA.value

    def w_dol(self):
        """zwraca nowe położenie przesunięte w dół"""
        return self + Kierunek.DOL.value

    def w_lewo_gore(self):
        """zwraca nowe położenie przesunięte w lewo i w górę"""
        return self + Kierunek.LEWO_GORA.value

    def w_lewo_dol(self):
        """zwraca nowe położenie przesunięte w lewo i  w dół"""
        return self + Kierunek.LEWO_DOL.value

    def w_prawo_gore(self):
        """zwraca nowe położenie przesunięte w prawo i w górę"""
        return self + Kierunek.PRAWO_GORA.value

    def w_prawo_dol(self):
        """zwraca nowe położenie przesunięte w prawo i w dół"""
        return self + Kierunek.PRAWO_DOL.value

    def __getitem__(self, key):
        return self.poz[key]

_wszystkie = None
class Siatka:
    """reprezentuje siatkę na której gracze stawiają symbole"""
    def __init__(self, wierszy=15, kolumn=15):
        global _wszystkie
        self.pola = {}
        self.wierszy = wierszy
        self.kolumn = kolumn
        self._liczba_pol = kolumn * wierszy
        if _wszystkie is None:
            _wszystkie = list(itertools.product(range(self.wierszy),
                                            range(self.kolumn)))

    def __repr_wiersz(self, num_wiersz):
        return [self[Polozenie(num_wiersz, num_kol)].repr
                for num_kol in range(self.kolumn)]

    def __repr__(self):
        bufor = []
        for num_wiersza in range(self.wierszy):
            bufor.extend(self.__repr_wiersz(num_wiersza))
            bufor.append("\n")
        return "".join(bufor)

    def zawiera_polozenie(self, polozenie):
        """czy dane położenie znajduje się na siatce czy poza nią"""
        wiersz, kolumna = polozenie
        return 0 <= wiersz < self.wierszy and 0 <= kolumna < self.kolumn

    __slownik = {'x': symbol.Krzyzyk, 'o': symbol.Kolko, '.': symbol.Puste}
    def _wczytaj_linie_na_wiersz(self, linia, numer_wiersza):
        bufor = []
        for sym in linia:
            bufor.append(Siatka.__slownik[sym])
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
        wyjscie = Siatka(self.wierszy, self.kolumn)
        wyjscie.pola = self.pola.copy()
        return wyjscie

    def __getitem__(self, polozenie):     
        return self.pola.get(polozenie, symbol.Puste)

    def __setitem__(self, polozenie, symbol_gracza):
        self.pola[polozenie] = symbol_gracza

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

    def __ma_uklad_wygrywajacy_w_kierunkach(self, polozenie,
                                            kierunki):
        symbol_sprawdzany = self[polozenie]
        #kierunek1
        licznik1 = self.__zliczaj_symbole_w_kierunku(symbol_sprawdzany,
                                                     polozenie,
                                                     kierunki[0])
        #kierunek2
        polozenie = (Siatka.__kierunki[kierunki[1]])(polozenie)
        licznik2 = self.__zliczaj_symbole_w_kierunku(symbol_sprawdzany,
                                                     polozenie,
                                                     kierunki[1])
        return (licznik1 + licznik2) >= WYGRYWAJACYCH
    __strony = (('w_prawo', 'w_lewo'), #poziom
                ('w_dol', 'w_gore'), #pion
                ('w_prawo_dol', 'w_lewo_gore'), #ukos_lewy
                ('w_lewo_dol', 'w_prawo_gore') #ukos_prawy
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
        wszystkie = _wszystkie
        for para in wszystkie:
            ruch = Polozenie(*para)
            if not self.__zajeta(ruch):
                yield ruch

    __kierunki = {'w_lewo': Polozenie.w_lewo,
                  'w_prawo': Polozenie.w_prawo,
                  'w_dol' : Polozenie.w_dol,
                  'w_gore': Polozenie.w_gore,
                  'w_prawo_dol': Polozenie.w_prawo_dol,
                  'w_lewo_gore': Polozenie.w_lewo_gore,
                  'w_prawo_gore': Polozenie.w_prawo_gore,
                  'w_lewo_dol': Polozenie.w_lewo_dol,}

    def __zliczaj_symbole_w_kierunku(self, symbol_gracza, polozenie,
                                     kierunek):
        licznik = 0
        idz_w_kierunku = Siatka.__kierunki[kierunek]
        while self.zawiera_polozenie(polozenie):
            if self[polozenie] == symbol_gracza:
                licznik += 1
                polozenie = idz_w_kierunku(polozenie)
            else:
                break
        return licznik
