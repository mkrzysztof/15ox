"""Gra"""
#import renderowanie
from grafika import odczyt_poz_myszy, rysuj_siatke, Kolko_graf, Krzyzyk_graf
import pygame

def pokaz_wywolanie(f):
    def opakowanie(*args, **kwds):
        print('wywołuję: ', f.__name__)
        return f(*args, **kwds)
    return opakowanie

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

class Siatka:
    def __init__(self, wierszy=15, kolumn = 15):
        self.pola = [[None for x in range(kolumn)] for y in range(wierszy)]

    def odczyt_pozycja(self, wiersz, kolumna):
        return self.pola[wiersz][kolumna]

    def zapis_pozycja(self, wiersz, kolumna, sym):
        self.pola[wiersz][kolumna] = sym
    
class Polozenie(object):
    """ pozycja """
    def __init__(self, wiersz, kolumna):
        self.poz = [wiersz, kolumna]

    @pokaz_wywolanie
    def w_lewo(self):
        self.poz[1] -= 1

    @pokaz_wywolanie
    def w_prawo(self):
        self.poz[1] += 1

    @pokaz_wywolanie
    def w_gore(self):
        self.poz[0] -= 1

    @pokaz_wywolanie
    def w_dol(self):
        self.poz[0] += 1

    def __getitem__(self, key):
        return self.poz[key]

    def nie_wychodzi_poza(self, plansza):
        """ sprawdza xzy położenie wychodzi poza planszę """
        wiersz = 0
        kolumna = 1
        wyj = (self[wiersz] >= 0
               or self[wiersz] < plansza.wierszy
               or self[kolumna] >= 0
               or self[kolumna] < plansza.kolumn)
        return wyj
    
class Plansza:
    """reprentuje prostokątną planszę na której stawiane są kółka lub
    krzyżyki
    """

    def __init__(self, surface, wierszy=15, kolumn=15):
        self.pola = Siatka(wierszy, kolumn)
        self.wierszy = wierszy
        self.kolumn = kolumn
        self.surface = surface

    def postaw_na_pozycji_symbol(self, poz, symbol):
        self.pola.zapis_pozycja(*poz, symbol)
        print(poz)

    @pokaz_wywolanie
    def jest_zapelniona(self):
        zap = True
        def zajeta(nr_wiersza, nr_kolumny):
            pola = self.pola
            symbol = pola.odczyt_pozycja(nr_wiersza, nr_kolumny)
            return symbol is not None
        for nr_wiersza in range(self.wierszy):
            for nr_kolumny in range(self.kolumn):
                zap = zap  and zajeta(nr_wiersza, nr_kolumny)
        return zap

    def ma_uklad_wygrywajacy(self, pozycja):
        """szukaj układu wygrywającego wokół pozycji pozycja,
        w 4 kierunkach
        """
        pytania = []
        pytania.extend([self.ma_uklad_wygrywajacy_pion(pozycja),
                        self.ma_uklad_wygrywajacy_poziom(pozycja)])
        return any(pyt for pyt in pytania)


    def pasuje_pozycja_symbol(self, nr_wiersza, nr_kolumny, symbol):
        pola = self.pola
        return pola.odczyt_pozycja(nr_wiersza, nr_kolumny) == symbol

    @pokaz_wywolanie
    def ma_uklad_wygrywajacy_poziom(self, pozycja):
        kolumna = 1
        wiersz = 0
        pola = self.pola
        polozenie = Polozenie(*pozycja)
        symbol = pola.odczyt_pozycja(*polozenie)
        licznik = 0
        #idź w prawo
        while (polozenie.nie_wychodzi_poza(self)
               and self.pasuje_pozycja_symbol(*polozenie, symbol)):
            licznik += 1
            polozenie.w_prawo()
        # bteraz w lewo
        polozenie = Polozenie(*pozycja)
        polozenie.w_lewo()
        while (polozenie.nie_wychodzi_poza(self)
               and self.pasuje_pozycja_symbol(*polozenie, symbol)):
            licznik += 1
            polozenie.w_lewo()
        if licznik >= 5:
            print('ma_uklad_wygrywajacy_poziom')
        return licznik >= 5

    @pokaz_wywolanie
    def ma_uklad_wygrywajacy_pion(self, pozycja):
        wiersz = 0
        kolumna = 1
        pola = self.pola
        polozenie = Polozenie(*pozycja)
        symbol = pola.odczyt_pozycja(*pozycja)
        licznik = 0
        nr_wiersza, nr_kolumny = pozycja
        spr_wiersz = nr_wiersza
        #idź w dół
        while (polozenie[wiersz] < self.wierszy
               and self.pasuje_pozycja_symbol(*polozenie, symbol)):
            licznik += 1
            polozenie.w_dol()
        #idź w górę
        polozenie = Polozenie(*pozycja)
        polozenie.w_gore()
        while (polozenie[wiersz] >= 0
               and self.pasuje_pozycja_symbol(*polozenie, symbol)):
            licznik += 1
            polozenie.w_gore()
        if licznik >= 5:
            print('ma_uklad_wygrywajacy_pion')
        return licznik >= 5

    @pokaz_wywolanie
    def ma_uklad_wygrywajacy_ukos_lewy(self, pozycja):
        pola = self.pola
        symbol = pola.odczyt_pozycja(*pozycja)
        nr_wiersza, nr_kolumny = pozycja
        spr_wiersz, spr_kolumna = nr_wiersza, nr_kolumny
        licznik = 0
        while (spr_wiersz < self.wierszy and
               spr_kolumna < self.kolumn and
               self.pasuje_pozycja_symbol(spr_wiersz, spr_kolumna, symbol)):
            licznik += 1
            spr_wiersz, spr_kolumna = spr_wiersz + 1, spr_kolumna + 1
        #idź w górę
        spr_wiersz, spr_kolumna = nr_wiersza - 1, nr_kolumny - 1
        while (spr_wiersz >= 0 and spr_kolumna >= 0 and
               self.pasuje_pozycja_symbol(spr_wiersz, nr_kolumny, symbol)):
            licznik += 1
            spr_wiersz -= 1
            spr_kolumna -= 1
        if licznik >= 5:
            print('ma_uklad_wygrywajacy_ukos_lewy')
        return licznik >= 5
    
    def ma_uklad_wygrywajacy_ukos_prawy(self, pozycja):
        pass


class Gracz(object):
    """Klasa abstrakcyjna reprezentująca dowoilnego gracza"""
    def __init__(self, symbol):
        self.symbol = symbol
        self.wygrana = False
                                       

    def wyszukaj_wolne_pole(self, plansza):
        """metoda obstrakcyjna zwraca 2-kę reprezentującą położenie
        na polu planszy w formacie [nr_wiersza, nr_kolumny]"""
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
