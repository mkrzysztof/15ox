"""Gra"""
#import renderowanie
from grafika import odczyt_poz_myszy, rysuj_siatke, Kolko_graf, Krzyzyk_graf
import pygame
from siatka import Siatka, Polozenie
import zarzadca

#stałe
WIERSZ = 0
KOLUMNA = 1

def pokaz_wywolanie(fun):
    """raportuje wuwołanie funkcjii do adnotacji"""
    def __opakowanie(*args, **kwds):
        print('wywołuję: ', fun.__name__)
        return fun(*args, **kwds)
    return __opakowanie

class Symbol(object):
    """klasa abstrakcyjna reprezentująca kółko lub krzyżykl"""
    repr_graf = None
    repr = None

    @classmethod
    def postaw_na_planszy(cls, plansza, polozenie):
        """postaw na planszy symbol na pozycji"""
        pozycja = tuple(polozenie)
        plansza.zapis_polozenie(polozenie, cls)
        zarzadca.rozeslij(pozycja, plansza.surface, cls.repr_graf)

class Kolko(Symbol):
    """sybol kółka"""
    repr_graf = Kolko_graf()
    repr = "Kolko"

class Krzyzyk(Symbol):
    """symbol krzyżyk"""
    repr_graf = Krzyzyk_graf()
    repr = "Krzyzyk"

class Plansza:
    """reprezentuje planszę na której rozgrywana jest gra:
    siatka gry + informacje"""

    def __init__(self, surface, wierszy=15, kolumn=15):
        """ surface obiekt pygame.surface """
        self.pola = Siatka(wierszy, kolumn)
        self.wierszy = wierszy
        self.kolumn = kolumn
        self.surface = surface

    def zapis_polozenie(self, polozenie, symbol):
        """postawienie symbol na Plansza na polozenie"""
        self.pola.zapis_polozenie(polozenie, symbol)

    def jest_zapelniona(self):
        return self.pola.jest_zapelniona()

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        return self.pola.ma_uklad_wygrywajacy(polozenie)

class Gracz(object):
    """Klasa abstrakcyjna reprezentująca dowoilnego gracza"""
    def __init__(self, symbol):
        self.symbol = symbol
        self.wygrana = False
        self.mnoznik = 0
        self.przeciwnik = None

    def wyszukaj_wolne_pole(self, plansza):
        """metoda obstrakcyjna zwraca siatka.Polozenie reprezentującą położenie
        na polu planszy """
        pass

    def postaw_symbol_na_planszy(self, plansza):
        polozenie = self.wyszukaj_wolne_pole(plansza)
        self.symbol.postaw_na_planszy(plansza, polozenie)
        return polozenie

    def ustaw_wygrana(self):
        self.wygrana = True
        print("wygrana")


class GraczCzlowiek(Gracz):
    """Klasa reprezentująca człowieka"""

    def wyszukaj_wolne_pole(self, plansza):
        zla_pozycja = True
        while zla_pozycja:
            polozenie = odczyt_poz_myszy()
            if (polozenie.nie_wychodzi_poza(plansza.pola)
                    and polozenie.jest_puste(plansza.pola)):
                zla_pozycja = False
        return polozenie

class GraczKomputer(Gracz):
    """Klasa reprezentująca komputer"""
    pass

def gra(pierwszy_gracz, drugi_gracz, plansza):
    """Główna procedura rozgrywki"""
    # dopuki któryś z graczy nie wygra lub jest remis:\
    # bieżący gracz stawia swój symbol na wolnym polu planszsy\
    # jeżeli wykryrto układ wygrywający zgłoś wygraną bieżącego gracza\
    # w pp jeśli plansza zapełniona zgłoś remis\
    # w pp zmień bieżącego gracza
    remis = False
    gracze = (pierwszy_gracz, drugi_gracz)
    num_gracza = 0
    while not (pierwszy_gracz.wygrana or drugi_gracz.wygrana or remis):
        biezacy_gracz = gracze[num_gracza]
        polozenie = biezacy_gracz.postaw_symbol_na_planszy(plansza)
        if plansza.ma_uklad_wygrywajacy(polozenie):
            biezacy_gracz.ustaw_wygrana()
        elif plansza.jest_zapelniona():
            remis = True
        else:
            num_gracza = (num_gracza + 1) % 2

if __name__ == "__main__":
    pygame.init()
    SURFACE = pygame.display.set_mode((800, 600))
    PLANSZA = Plansza(SURFACE)
    PLANSZA_ROZMIAR = (15, 15)
    rysuj_siatke(PLANSZA_ROZMIAR, SURFACE)
    GRACZ1 = GraczCzlowiek(Kolko)
    GRACZ2 = GraczCzlowiek(Krzyzyk)
    GRACZ1.przeciwnik = GRACZ2
    GRACZ2.przeciwnik = GRACZ1
    gra(GRACZ1, GRACZ2, PLANSZA)
