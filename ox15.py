"""Gra"""
#import renderowanie
from grafika import odczyt_poz_myszy, rysuj_siatke, Kolko_graf, Krzyzyk_graf
import pygame

class Symbol(object):
    """klasa abstrakcyjna reprezentująca kółko lub krzyżykl"""
    repr_graf = None

    @classmethod
    def postaw_na_planszy(cls, plansza, pozycja):
        """postaw na planszy symbol na pozycji"""
        plansza.postaw_na_pozycji_symbol(pozycja, cls)
        cls.repr_graf.rysuj_na_pozycji(pozycja, plansza.surface)


class Kolko(Symbol):
    """sybol kółka"""
    repr_graf = Kolko_graf()

class Krzyzyk(Symbol):
    """symbol krzyżyk"""
    repr_graf = Krzyzyk_graf()

class __Siatka:
    def __init__(wierszy=15, kolumn = 15):
        self.pola = [[None for x in range(kolumn)] for y in range(wierszy)]

    def odczyt_pozycja(self, wiersz, kolumna):
        return self.pola[wiersz][kolumna]

    def zapis_pozycja(self, wiersz, kolumna, sym):
        self.pola[wiersz][kolumna] = sym

class Plansza:
    """reprentuje prostokątną planszę na której stawiane są kółka lub
    krzyżyki
    """

    def __init__(self, surface, wierszy=15, kolumn=15):
        self.pola = __Siatka(wierszy, kolumn)
        self.wierszy = wierszy
        self.kolumn = kolumn
        self.surface = surface

    def postaw_na_pozycji_symbol(self, poz, symbol):
        pola.zapis_pozycja(*poz, symbol)

    def jest_zapelniona(self):
        zap = True
        for wiersz in self.pola:
            zap = zap and all(kol is not None for kol in wiersz)
        return zap

    def ma_uklad_wygrywajacy(self, pozycja):
        """szukaj układu wygrywającego wokół pozycji pozycja,
        w 4 kierunkach
        """
        pytania = []
        pytania.extend([self.ma_uklad_wygrywajacy_pion(pozycja),
                        self.ma_uklad_wygrywajacy_poziom(pozycja),
                        self.ma_uklad_wygrywajacy_ukos_lewy(pozycja),
                        self.ma_uklad_wygrywajacy_ukos_prawy(pozycja)])
        return any(pyt for pyt in pytania)

    def ma_uklad_wygrywajacy_poziom(self, pozycja):
        symbol = self.pola[pozycja[0]][pozycja[1]]
        licznik = 0
        def pasuje():
            return self.pola[pozycja[0]][nr_kolumny] == symbol
        #idź w prawo
        nr_kolumny = pozycja[1]
        while nr_kolumny < self.kolumn and pasuje():
            licznik += 1
            nr_kolumny += 1
        # bteraz w lewo
        nr_kolumny = pozycja[1] - 1
        while nr_kolumny >= 0 and pasuje():
            licznik += 1
            nr_kolumny -= 1
        return licznik >= 5

    def ma_uklad_wygrywajacy_pion(self, pozycja):
        symbol = self.pola[pozycja[0]][pozycja[1]]
        licznik = 0
        nr_wiersza, nr_kolumny = pozycja
        def pasuje():
            return self.pola[nr_wiersza][nr_kolumny] == symbol
        #idź w dół
        while nr_wiersza < self.wierszy and pasuje():
            licznik += 1
            nr_wiersza += 1
        #idź w górę
        nr_wiersza, nr_kolumny = pozycja
        while nr_wiersza >= 0 and pasuje():
            licznik += 1
            nr_wiersza -= 1
        return licznik >= 5

    def ma_uklad_wygrywajacy_ukos_lewy(self, pozycja):
        symbol = self.pola[pozycja[0]][pozycja[1]]
        nr_wiersza, nr_kolumny = pozycja
        licznik = 0
        def pasuje(nr_wiersza, nr_kolumny):
            return self.pola[nr_wiersza][nr_kolumny] == symbol
        while (nr_wiersza < self.wierszy and
               nr_kolumny < self.kolumn and
               pasuje(nr_wiersza, nr_kolumny)):
            licznik += 1
            nr_wiersza += 1
            nr_kolumny += 1
        #idź w górę
        nr_wiersza, nr_kolumny = pozycja
        while (nr_wiersza >= 0 and nr_kolumny >= 0 and
               pasuje(nr_wiersza, nr_kolumny)):
            licznik += 1
            nr_wiersza -= 1
            nr_kolumny -= 1

    def ma_uklad_wygrywajacy_ukos_prawy(self, pozycja):
        pass


class Gracz(object):
    """Klasa abstrakcyjna reprezentująca dowoilnego gracza"""
    def __init__(self, symbol):
        self.symbol = symbol
        self.wygrana = False
                                       

    def wyszukaj_wolne_pole(self, plansza):
        """metoda obstrakcyjna zwraca 2-kę reprezentującą położenie
        na polu planszy"""
        pass

    def postaw_symbol_na_planszy(self, plansza):
        pozycja = self.wyszukaj_wolne_pole(plansza)
        self.symbol.postaw_na_planszy(plansza, pozycja)
        return pozycja

    def ustaw_wygrana(self):
        self.wygrana = True
        print("wygrana")


class Gracz_Czlowiek(Gracz):
    """Klasa reprezentująca człowieka"""
    def wyszukaj_wolne_pole(self, plansza):
        return odczyt_poz_myszy()


class Gracz_komputer(Gracz):
    pass

def gra(pierwszy_gracz, drugi_gracz, plansza):
    """Główna procedura rozgrywki"""
    "dopuki któryś z graczy nie wygra lub jest remis:\
        bieżący gracz stawia swój symbol na wolnym polu planszsy\
        jeżeli wykryrto układ wygrywający zgłoś wygraną bieżącego gracza\
        w pp jeśli plansza zapełniona zgłoś remis\
        w pp zmień bieżącego gracza\
    "
    remis = False
    gracze = (pierwszy_gracz, drugi_gracz)
    num_gracza = 0
    while not (pierwszy_gracz.wygrana or drugi_gracz.wygrana or remis):
        biezacy_gracz = gracze[num_gracza]
        pozycja = biezacy_gracz.postaw_symbol_na_planszy(plansza)
        if plansza.ma_uklad_wygrywajacy(pozycja):
            biezacy_gracz.ustaw_wygrana()
        elif plansza.jest_zapelniona():
            remis = True
        else:
            num_gracza = (num_gracza + 1) % 2

if __name__ == "__main__":
    surface = pygame.display.set_mode((800, 600))
    plansza = Plansza(surface)
    plansza_rozmiar = (15, 15)
    rysuj_siatke(plansza_rozmiar, surface)
    gracz1 = Gracz_Czlowiek(Kolko)
    gracz2 = Gracz_Czlowiek(Krzyzyk)

    gra(gracz1, gracz2, plansza)
