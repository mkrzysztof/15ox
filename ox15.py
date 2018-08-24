"""Gra"""
#import renderowanie
from grafika import odczyt_poz_myszy, rysuj_siatke, Kolko_graf, Krzyzyk_graf
import pygame
from siatka import Siatka, Polozenie

#stałe
WIERSZ = 0
KOLUMNA = 1

def pokaz_wywolanie(fun):
    """raportuje wuwołanie funkcjii do adnotacji"""
    def opakowanie(*args, **kwds):
        print('wywołuję: ', fun.__name__)
        return fun(*args, **kwds)
    return opakowanie

class Symbol(object):
    """klasa abstrakcyjna reprezentująca kółko lub krzyżykl"""
    repr_graf = None

    @classmethod
    def postaw_na_planszy(cls, plansza, polozenie):
        """postaw na planszy symbol na pozycji"""
        pozycja = tuple(polozenie)
        plansza.zapis_polozenie(polozenie, cls)
        cls.repr_graf.rysuj_na_pozycji(pozycja, plansza.surface)

class Kolko(Symbol):
    """sybol kółka"""
    repr_graf = Kolko_graf()

class Krzyzyk(Symbol):
    """symbol krzyżyk"""
    repr_graf = Krzyzyk_graf()


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
        """sprawdza czy plansza jest całkowicie wypełniona"""
        zap = True
        def zajeta(polozenie):
            pola = self.pola
            symbol = pola.odczyt_polozenie(polozenie)
            return symbol is not None
        for nr_wiersza in range(self.wierszy):
            for nr_kolumny in range(self.kolumn):
                zap = zap  and zajeta(Polozenie(nr_wiersza, nr_kolumny))
        return zap

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        return (self.__ma_uklad_wygrywajacy_pion(polozenie)
                or self.__ma_uklad_wygrywajacy_poziom(polozenie)
                or self.__ma_uklad_wygrywajacy_ukos_lewy(polozenie)
                or self.__ma_uklad_wygrywajacy_ukos_prawy(polozenie))

    def __pasuje_pozycja_symbol(self, polozenie, symbol):
        pola = self.pola
        return pola.odczyt_polozenie(polozenie) == symbol
    
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
        while polozenie.nie_wychodzi_poza(self.pola):
            if self.__pasuje_pozycja_symbol(polozenie, symbol):
                licznik += 1
                polozenie = (Plansza.__kierunki[kierunek])(polozenie)
            else:
                break
        return licznik

    def __ma_uklad_wygrywajacy_w_kierunkach(self, polozenie,
                                            kierunek1, kierunek2):
        symbol = self.pola.odczyt_polozenie(polozenie)
        #kierunek1
        licznik1 = self.__zliczaj_symbole_w_kierunku(symbol, polozenie,
                                                     kierunek1)
        #kierunek2
        polozenie = (Plansza.__kierunki[kierunek2])(polozenie)
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

class Gracz(object):
    """Klasa abstrakcyjna reprezentująca dowoilnego gracza"""
    def __init__(self, symbol):
        self.symbol = symbol
        self.wygrana = False

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
    gra(GRACZ1, GRACZ2, PLANSZA)
