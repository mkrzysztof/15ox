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

    def __str__(self):
        return str(self.poz)

    def w_lewo(self):
        self.poz[1] -= 1

    def w_prawo(self):
        self.poz[1] += 1

    def w_gore(self):
        self.poz[0] -= 1


    def w_dol(self):
        self.poz[0] += 1

    @pokaz_wywolanie
    def w_lewo_gore(self):
        self.w_lewo()
        self.w_gore()

    @pokaz_wywolanie
    def w_lewo_dol(self):
        self.w_lewo()
        self.w_dol()

    @pokaz_wywolanie
    def w_prawo_gore(self):
        self.w_prawo()
        self.w_gore()

    @pokaz_wywolanie
    def w_prawo_dol(self):
        self.w_prawo()
        self.w_dol()

    def __getitem__(self, key):
        return self.poz[key]

    def nie_wychodzi_poza(self, plansza):
        """ sprawdza xzy położenie wychodzi poza planszę """
        wiersz = 0
        kolumna = 1
        wyj = (self[wiersz] >= 0
               and self[wiersz] < plansza.wierszy
               and self[kolumna] >= 0
               and self[kolumna] < plansza.kolumn)
        return wyj

    def jest_puste(self, plansza):
        """ sprawdza czy polozenie na plansza jest puste """
        wiersz = 0
        kolumna = 1
        return plansza.pola.odczyt_pozycja(*self) is None
    
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
                        self.ma_uklad_wygrywajacy_poziom(pozycja),
                        self.ma_uklad_wygrywajacy_ukos_lewy(pozycja),
                        self.ma_uklad_wygrywajacy_ukos_prawy(pozycja)])
        return any(pyt for pyt in pytania)

    def pasuje_pozycja_symbol(self, nr_wiersza, nr_kolumny, symbol):
        pola = self.pola
        return pola.odczyt_pozycja(nr_wiersza, nr_kolumny) == symbol

    def zliczaj_symbole_w_kierunku(self, symbol, polozenie,
                                   kierunek, licznik):
        while polozenie.nie_wychodzi_poza(self):
            if self.pasuje_pozycja_symbol(*polozenie, symbol):
                licznik[0] += 1
                kierunek()
            else:
                break

    def ma_uklad_wygrywajacy_poziom(self, pozycja):
        polozenie = Polozenie(*pozycja)
        symbol = self.pola.odczyt_pozycja(*polozenie)
        licznik = [0]
        #idź w prawo
        self.zliczaj_symbole_w_kierunku(symbol, polozenie,
                                        polozenie.w_prawo, licznik)
        # bteraz w lewo
        polozenie = Polozenie(*pozycja)
        polozenie.w_lewo()
        self.zliczaj_symbole_w_kierunku(symbol, polozenie,
                                        polozenie.w_lewo, licznik)
        return licznik[0] >= 5


    def ma_uklad_wygrywajacy_pion(self, pozycja):
        polozenie = Polozenie(*pozycja)
        symbol = self.pola.odczyt_pozycja(*pozycja)
        licznik = [0]
        #idź w dół
        self.zliczaj_symbole_w_kierunku(symbol, polozenie,
                                        polozenie.w_dol, licznik)
        #idź w górę
        polozenie = Polozenie(*pozycja)
        polozenie.w_gore()
        self.zliczaj_symbole_w_kierunku(symbol, polozenie,
                                        polozenie.w_gore, licznik)
        if licznik[0] >= 5:
            print('ma_uklad_wygrywajacy_pion')
        return licznik[0] >= 5

    @pokaz_wywolanie
    def ma_uklad_wygrywajacy_ukos_lewy(self, pozycja):
        polozenie = Polozenie(*pozycja)
        symbol = self.pola.odczyt_pozycja(*polozenie)
        licznik = [0]
        #idź lewo dół
        self.zliczaj_symbole_w_kierunku(symbol, polozenie,
                                        polozenie.w_prawo_dol, licznik)
        #idź w lewo górę
        polozenie = Polozenie(*pozycja)
        polozenie.w_lewo_gore()
        self.zliczaj_symbole_w_kierunku(symbol, polozenie,
                                        polozenie.w_lewo_gore, licznik)
        return licznik[0] >= 5
    @pokaz_wywolanie
    def ma_uklad_wygrywajacy_ukos_prawy(self, pozycja):
        polozenie = Polozenie(*pozycja)
        symbol = self.pola.odczyt_pozycja(*polozenie)
        licznik = [0]
        #idź w dół
        self.zliczaj_symbole_w_kierunku(symbol, polozenie,
                                        polozenie.w_lewo_dol, licznik)
        print(licznik)
        # idź w górę
        polozenie = Polozenie(*pozycja)
        polozenie.w_prawo_gore()
        self.zliczaj_symbole_w_kierunku(symbol, polozenie,
                                        polozenie.w_prawo_gore, licznik)
        print(licznik)
        return licznik[0] >= 5

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
    @pokaz_wywolanie
    def wyszukaj_wolne_pole(self, plansza):
        zla_pozycja = True
        while zla_pozycja:
            pozycja = odczyt_poz_myszy()
            polozenie = Polozenie(*pozycja)
            if (polozenie.nie_wychodzi_poza(plansza)
                and polozenie.jest_puste(plansza)):
                zla_pozycja = False
        return pozycja
            

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
