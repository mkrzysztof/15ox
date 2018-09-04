""" Moduł zawiera fefinicję klas Polozenie i Siatka"""
import itertools

#stałe
WIERSZ = 0
KOLUMNA = 1

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
        return siatka.odczyt_polozenie(self) is None

class Siatka:
    """reprezentuje siatkę na której gracze stawiają symbole"""
    def __init__(self, wierszy=15, kolumn=15):
        self.pola = [[None for x in range(kolumn)] for y in range(wierszy)]
        self.wierszy = wierszy
        self.kolumn = kolumn

    def odczyt_polozenie(self, polozenie):
        """odczytuje symbol z położenia"""
        wiersz, kolumna = polozenie
        return self.pola[wiersz][kolumna]

    def zapis_polozenie(self, polozenie, symbol):
        """stawia symbol na położenie"""
        wiersz, kolumna = polozenie
        self.pola[wiersz][kolumna] = symbol

    def __zajete(self, polozenie):
        symbol = self.odczyt_polozenie(polozenie)
        return symbol is not None
        
    def jest_zapelniona(self):
        """sprawdza czy plansza jest całkowicie wypełniona"""
        zap = True
        for nr_wiersza in range(self.wierszy):
            for nr_kolumny in range(self.kolumn):
                zap = zap  and self.__zajeta(Polozenie(nr_wiersza, nr_kolumny))
        return zap

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        return (self.__ma_uklad_wygrywajacy_pion(polozenie)
                or self.__ma_uklad_wygrywajacy_poziom(polozenie)
                or self.__ma_uklad_wygrywajacy_ukos_lewy(polozenie)
                or self.__ma_uklad_wygrywajacy_ukos_prawy(polozenie))

    def wolne_pola(self):
        """ zwraca generator wolnych pól siatki"""
        wszystkie = itertools.product(range(self.wierszy), range(self.kolumn))
        for para in wszystkie:
            ruch = Polozenie(*para)
            if not self.__zajete(ruch):
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
        while polozenie.nie_wychodzi_poza(self):
            if self.__pasuje_pozycja_symbol(polozenie, symbol):
                licznik += 1
                polozenie = (Siatka.__kierunki[kierunek])(polozenie)
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
        return (licznik1 + licznik2) >= 5

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


