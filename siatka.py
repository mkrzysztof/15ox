""" Moduł zawiera fefinicję klas Polozenie i Siatka"""
import itertools
import symbol

#stałe
WIERSZ = 0
KOLUMNA = 1
WYGRYWAJACYCH = 3

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
        return (0 <= self[WIERSZ] < siatka.wierszy
                and 0 <= self[KOLUMNA] < siatka.kolumn)

    def jest_puste(self, siatka):
        """ sprawdza czy polozenie na plansza jest puste """
        return siatka.odczyt_polozenie(self) == symbol.Puste

class Siatka:
    """reprezentuje siatkę na której gracze stawiają symbole"""
    def __init__(self, wierszy=15, kolumn=15):
        self.pola = [[symbol.Puste] * kolumn for y in range(wierszy)]
        self.wierszy = wierszy
        self.kolumn = kolumn


    def __repr_wiersz(self, num_wiersz):
        return [self.odczyt_polozenie(Polozenie(num_wiersz, num_kol)).repr
                for num_kol in range(self.kolumn)]

    def __repr__(self):
        bufor = []
        for num_wiersza in range(self.wierszy):
            bufor.extend(self.__repr_wiersz(num_wiersza))
            bufor.append("\n")
        return "".join(bufor)

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
        wyj_pola = wyjscie.pola
        for numer, wiersz in enumerate(self.pola):
            wyj_pola[numer] = wiersz[:]
        return wyjscie

    def odczyt_polozenie(self, polozenie):
        """odczytuje symbol z położenia"""
        return self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]]

    def zapis_polozenie(self, polozenie, symbol_gracza):
        """stawia symbol na położenie"""
        self.pola[polozenie[WIERSZ]][polozenie[KOLUMNA]] = symbol_gracza

    def __zajeta(self, polozenie):
        odczytany_symbol = self.odczyt_polozenie(polozenie)
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
        zap = True
        for wiersz in self.pola:
            zap = zap and (Siatka._wiersz_jest_zapelniony(wiersz))
            if not zap:
                break
        return zap

    def __ma_uklad_wygrywajacy_w_kierunkach(self, polozenie,
                                            kierunki):
        symbol_sprawdzany = self.odczyt_polozenie(polozenie)
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
        wszystkie = itertools.product(range(self.wierszy), range(self.kolumn))
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
        while polozenie.nie_wychodzi_poza(self):
            if self.odczyt_polozenie(polozenie) == symbol_gracza:
                licznik += 1
                polozenie = idz_w_kierunku(polozenie)
            else:
                break
        return licznik
