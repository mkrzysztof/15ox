""" Moduł zawiera fefinicję klas Polozenie i Siatka"""

#stałe
WIERSZ = 0
KOLUMNA = 1

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
