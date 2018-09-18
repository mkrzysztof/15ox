""" Moduł zawiera fefinicję klas Polozenie i Siatka"""
import itertools
import symbol

#stałe
WIERSZ = 0
KOLUMNA = 1
_wygrywajacych = 3

class Polozenie(object):
    """reprezentuje położenie (wiersz, kolumna) """
    def __init__(self, wiersz, kolumna):
        self.poz = (wiersz, kolumna)

    def __str__(self):
        return str(self.poz)

    def w_lewo(self):
        """zwraca nowe położenie przesunięte w lewo"""
        return Polozenie(self.poz[WIERSZ], self.poz[KOLUMNA] - 1)

    def w_prawo(self):
        """zwraca nowe położenie przesunięte w prawo"""
        return Polozenie(self.poz[WIERSZ], self.poz[KOLUMNA] + 1)

    def w_gore(self):
        """zwraca nowe położenie przesunięte w górę"""
        return Polozenie(self.poz[WIERSZ] - 1, self.poz[KOLUMNA])


    def w_dol(self):
        """zwraca nowe położenie przesunięte w dół"""
        return Polozenie(self.poz[WIERSZ] + 1, self.poz[KOLUMNA])

    def w_lewo_gore(self):
        """zwraca nowe położenie przesunięte w lewo i w górę"""
        return self.w_lewo().w_gore()

    def w_lewo_dol(self):
        """zwraca nowe położenie przesunięte w lewo i  w dół"""
        return self.w_lewo().w_dol()

    def w_prawo_gore(self):
        """zwraca nowe położenie przesunięte w prawo i w górę"""
        return self.w_prawo().w_gore()

    def w_prawo_dol(self):
        """zwraca nowe położenie przesunięte w prawo i w dół"""
        return self.w_prawo().w_dol()

    def __getitem__(self, key):
        return self.poz[key]

    def nie_wychodzi_poza(self, siatka):
        """ sprawdza xzy położenie wychodzi poza planszę """
        wyj = (self[WIERSZ] >= 0
               and self[WIERSZ] < siatka.wierszy
               and self[KOLUMNA] >= 0
               and self[KOLUMNA] < siatka.kolumn)
        return wyj

    def jest_puste(self, siatka):
        """ sprawdza czy polozenie na plansza jest puste """
        return siatka.odczyt_polozenie(self) == symbol.Puste

class Siatka:
    """reprezentuje siatkę na której gracze stawiają symbole"""
    def __init__(self, wierszy=15, kolumn=15):
        self.pola = [[symbol.Puste] * kolumn for y in range(wierszy)]
        self.wierszy = wierszy
        self.kolumn = kolumn


    def __repr_wiersz(self, w):
        return [self.odczyt_polozenie(Polozenie(w, k)).repr
                 for k in range(self.kolumn)]

    def __repr__(self):
        repr = []
        for w in range(self.wierszy):
            repr.extend(self.__repr_wiersz(w))
            repr.append("\n")
        return "".join(repr)


    def _wczytaj_linie_na_wiersz(self, linia, numer_wiersza):
        repr = []
        slownik = {'x': symbol.Krzyzyk, 'o': symbol.Kolko,
                   '.': symbol.Puste}
        for sym in linia:
            repr.append(slownik[sym])
        self.pola[numer_wiersza] = repr
    
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
        for nr, wiersz in enumerate(self.pola):
            wyjscie.pola[nr] = wiersz.copy()
        return wyjscie

    def odczyt_polozenie(self, polozenie):
        """odczytuje symbol z położenia"""
        return self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]]

    def zapis_polozenie(self, polozenie, symbol):
        """stawia symbol na położenie"""
        self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]] = symbol

    def __zajeta(self, polozenie):
        odczytany_symbol = self.odczyt_polozenie(polozenie)
        return odczytany_symbol != symbol.Puste

    def _wiersz_jest_zapelniony(wiersz):
        zap = True
        for s in wiersz:
            zap = zap and (s != symbol.Puste)
            if not zap: break
        return zap

    def jest_zapelniona(self):
        """sprawdza czy plansza jest całkowicie wypełniona"""
        zap = True
        for wiersz in self.pola:
            zap = zap and (Siatka._wiersz_jest_zapelniony(wiersz))
            if not zap: break
        return zap

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        wyj = False
        if self.__ma_uklad_wygrywajacy_pion(polozenie):
            wyj = True
        elif self.__ma_uklad_wygrywajacy_poziom(polozenie):
            wyj = True
        elif self.__ma_uklad_wygrywajacy_ukos_lewy(polozenie):
            wyj = True
        elif self.__ma_uklad_wygrywajacy_ukos_prawy(polozenie):
            wyj = True
        return wyj

    def wolne_pola(self):
        """ zwraca generator wolnych pól (Polozenie) siatki """
        wszystkie = itertools.product(range(self.wierszy), range(self.kolumn))
        for para in wszystkie:
            ruch = Polozenie(*para)
            if not self.__zajeta(ruch):
                yield ruch

    def __pasuje_pozycja_symbol(self, polozenie, symbol):
        return self.odczyt_polozenie(polozenie) == symbol

    __kierunki = {'w_lewo': Polozenie.w_lewo,
                  'w_prawo': Polozenie.w_prawo,
                  'w_dol' : Polozenie.w_dol,
                  'w_gore': Polozenie.w_gore,
                  'w_prawo_dol': Polozenie.w_prawo_dol,
                  'w_lewo_gore': Polozenie.w_lewo_gore,
                  'w_prawo_gore': Polozenie.w_prawo_gore,
                  'w_lewo_dol': Polozenie.w_lewo_dol,}

    def __zliczaj_symbole_w_kierunku(self, symbol, polozenie,
                                     kierunek):
        licznik = 0
        idz_w_kierunku = Siatka.__kierunki[kierunek]
        while polozenie.nie_wychodzi_poza(self):
            if self.__pasuje_pozycja_symbol(polozenie, symbol):
                licznik += 1
                polozenie = idz_w_kierunku(polozenie)
            else:
                break
        return licznik

    def __ma_uklad_wygrywajacy_w_kierunkach(self, polozenie,
                                            kierunek1, kierunek2):
        symbol = self.odczyt_polozenie(polozenie)
        #kierunek1
        licznik1 = self.__zliczaj_symbole_w_kierunku(symbol, polozenie,
                                                     kierunek1)
        #kierunek2
        polozenie = (Siatka.__kierunki[kierunek2])(polozenie)
        licznik2 = self.__zliczaj_symbole_w_kierunku(symbol, polozenie,
                                                     kierunek2)
        return (licznik1 + licznik2) >= 3

    def __ma_uklad_wygrywajacy_poziom(self, polozenie):
        return self.__ma_uklad_wygrywajacy_w_kierunkach(polozenie,
                                                        'w_prawo', 'w_lewo')

    def __ma_uklad_wygrywajacy_pion(self, polozenie):
        return self.__ma_uklad_wygrywajacy_w_kierunkach(polozenie,
                                                        'w_dol', 'w_gore')
    def __ma_uklad_wygrywajacy_ukos_lewy(self, polozenie):
        return self.__ma_uklad_wygrywajacy_w_kierunkach(polozenie,
                                                        'w_prawo_dol',
                                                        'w_lewo_gore')

    def __ma_uklad_wygrywajacy_ukos_prawy(self, polozenie):
        return self.__ma_uklad_wygrywajacy_w_kierunkach(polozenie,
                                                        'w_lewo_dol',
                                                        'w_prawo_gore')


