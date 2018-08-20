"""Gra"""
#import renderowanie
from grafika import odczyt_poz_myszy, rysuj_siatke, Kolko_graf, Krzyzyk_graf
import pygame

#stałe
wiersz = 0
kolumna = 1

def pokaz_wywolanie(f):
    def opakowanie(*args, **kwds):
        print('wywołuję: ', f.__name__)
        return f(*args, **kwds)
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

class Siatka:
    def __init__(self, wierszy=15, kolumn = 15):
        self.pola = [[None for x in range(kolumn)] for y in range(wierszy)]

    def odczyt_polozenie(self, polozenie):
        wiersz, kolumna = polozenie
        return self.pola[wiersz][kolumna]

    def zapis_polozenie(self, polozenie, symbol):
        wiersz, kolumna = polozenie
        self.pola[wiersz][kolumna] = symbol
    
class Polozenie(object):
    """ pozycja """
    def __init__(self, wiersz, kolumna):
        self.poz = (wiersz, kolumna)

    def __str__(self):
        return str(self.poz)

    def w_lewo(self):
        return Polozenie(self.poz[wiersz], self.poz[kolumna] - 1)

    def w_prawo(self):
        return Polozenie(self.poz[wiersz], self.poz[kolumna] + 1)

    def w_gore(self):
        return Polozenie(self.poz[wiersz] - 1, self.poz[kolumna])


    def w_dol(self):
        return Polozenie(self.poz[wiersz] + 1, self.poz[kolumna])

    def w_lewo_gore(self):
        return self.w_lewo().w_gore()

    def w_lewo_dol(self):
        return self.w_lewo().w_dol()

    def w_prawo_gore(self):
        return self.w_prawo().w_gore()

    def w_prawo_dol(self):
        return self.w_prawo().w_dol()

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
        return plansza.pola.odczyt_polozenie(self) is None
    
class Plansza:
    """ reprezentuje planszę na której rozgrywana jest gra: 
    siatka gry + informacje"""
    
    def __init__(self, surface, wierszy=15, kolumn=15):
        self.pola = Siatka(wierszy, kolumn)
        self.wierszy = wierszy
        self.kolumn = kolumn
        self.surface = surface

    def zapis_polozenie(self, polozenie, symbol):
        self.pola.zapis_polozenie(polozenie, symbol)

    def jest_zapelniona(self):
        zap = True
        def zajeta(nr_wiersza, nr_kolumny):
            pola = self.pola
            symbol = pola.odczyt_polozenie(Polozenie(nr_wiersza, nr_kolumny))
            return symbol is not None
        for nr_wiersza in range(self.wierszy):
            for nr_kolumny in range(self.kolumn):
                zap = zap  and zajeta(nr_wiersza, nr_kolumny)
        return zap

    def ma_uklad_wygrywajacy(self, pozycja):
        """szukaj układu wygrywającego wokół pozycji pozycja,
        w 4 kierunkach
        """
        if (self.__ma_uklad_wygrywajacy_pion(pozycja)
            or self.__ma_uklad_wygrywajacy_poziom(pozycja)
            or self.__ma_uklad_wygrywajacy_ukos_lewy(pozycja)
            or self.__ma_uklad_wygrywajacy_ukos_prawy(pozycja)):
            return True
        else:
            return False

    def __pasuje_pozycja_symbol(self, nr_wiersza, nr_kolumny, symbol):
        pola = self.pola
        return pola.odczyt_polozenie(Polozenie(nr_wiersza, nr_kolumny)) == symbol
    __kierunki = {'w_lewo': Polozenie.w_lewo,
                'w_prawo': Polozenie.w_prawo,
                'w_dol' : Polozenie.w_dol,
                'w_gore': Polozenie.w_gore,
                'w_prawo_dol': Polozenie.w_prawo_dol,
                'w_lewo_gore': Polozenie.w_lewo_gore,
                'w_prawo_gore': Polozenie.w_prawo_gore,
                'w_lewo_dol': Polozenie.w_lewo_dol,
    }
                         
    
    def __zliczaj_symbole_w_kierunku(self, symbol, polozenie,
                                   kierunek):
        licznik = 0
        while polozenie.nie_wychodzi_poza(self):
            if self.__pasuje_pozycja_symbol(*polozenie, symbol):
                licznik += 1
                polozenie = (Plansza.__kierunki[kierunek])(polozenie)
            else:
                break
        return licznik

    def __ma_uklad_wygrywajacy_w_kierunkach(self, pozycja,
                                            kierunek1, kierunek2):
        polozenie = Polozenie(*pozycja)
        symbol = self.pola.odczyt_polozenie(polozenie)
        #kierunek1
        licznik1 = self.__zliczaj_symbole_w_kierunku(symbol, polozenie,
                                                     kierunek1)
        #kierunek2
        polozenie = Polozenie(*pozycja)
        polozenie = (Plansza.__kierunki[kierunek2])(polozenie)
        licznik2 = self.__zliczaj_symbole_w_kierunku(symbol, polozenie,
                                                     kierunek2)
        return (licznik1 + licznik2) >= 5

    def __ma_uklad_wygrywajacy_poziom(self, pozycja):
        return self.__ma_uklad_wygrywajacy_w_kierunkach(pozycja,
                                                      'w_prawo', 'w_lewo')

    def __ma_uklad_wygrywajacy_pion(self, pozycja):
        return self.__ma_uklad_wygrywajacy_w_kierunkach(pozycja,
                                                      'w_dol', 'w_gore')
    def __ma_uklad_wygrywajacy_ukos_lewy(self, pozycja):
        return self.__ma_uklad_wygrywajacy_w_kierunkach(pozycja,
                                                      'w_prawo_dol',
                                                      'w_lewo_gore')
    
    def __ma_uklad_wygrywajacy_ukos_prawy(self, pozycja):
        return self.__ma_uklad_wygrywajacy_w_kierunkach(pozycja,
                                                      'w_lewo_dol',
                                                      'w_prawo_gore')
        
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
        self.symbol.postaw_na_planszy(plansza, Polozenie(*pozycja))
        return pozycja

    def ustaw_wygrana(self):
        self.wygrana = True
        print("wygrana")


class Gracz_Czlowiek(Gracz):
    """Klasa reprezentująca człowieka"""

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
    pygame.init()
    surface = pygame.display.set_mode((800, 600))
    plansza = Plansza(surface)
    plansza_rozmiar = (15, 15)
    rysuj_siatke(plansza_rozmiar, surface)
    gracz1 = Gracz_Czlowiek(Kolko)
    gracz2 = Gracz_Czlowiek(Krzyzyk)
    gra(gracz1, gracz2, plansza)
