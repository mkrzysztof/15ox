import pygame
import siatka
import symbol
import zarzadca
import sys

# stałe
WIELKOSC = 20  # liczba pixeli przypadających na komórkę
odleglosc = WIELKOSC + 1
POCZATEK = (50, 50)
WIERSZ = 0
KOLUMNA = 1


pygame.init()


class Symbol_graf:
    """graficzna reprezentacja x lub o"""

    def rysuj_na_pozycji(self, pozycja, surface):
        poz_x = POCZATEK[KOLUMNA] + pozycja[KOLUMNA] * dlugosc
        poz_y = POCZATEK[WIERSZ] + pozycja[WIERSZ] * dlugosc
        surface.blit(self.sym, (poz_x, poz_y))
        pygame.display.flip()

    def __init__(self):
        self.font = pygame.font.SysFont("", 30)
        self.sym = None


class Kolko_graf(Symbol_graf):
    def __init__(self):
        super().__init__()
        self.sym = self.font.render('o', False, (0, 255, 0))
        self.sym = pygame.transform.scale(self.sym, (WIELKOSC, WIELKOSC))


class Krzyzyk_graf(Symbol_graf):
    def __init__(self):
        super().__init__()
        self.sym = self.font.render('x', False, (0, 255, 0))
        self.sym = pygame.transform.scale(self.sym, (WIELKOSC, WIELKOSC))


class Puste_graf(Symbol_graf):
    pass


reprezentacja = {symbol.Puste: Puste_graf(), symbol.Kolko: Kolko_graf(),
                 symbol.Krzyzyk: Krzyzyk_graf()}


def rysuj_na_pozycji(symbol, pozycja, surface):
        poz_x = POCZATEK[KOLUMNA] + pozycja[KOLUMNA] * odleglosc
        poz_y = POCZATEK[WIERSZ] + pozycja[WIERSZ] * odleglosc
        surface.blit(reprezentacja[symbol].sym, (poz_x, poz_y))
        pygame.display.flip()

zarzadca.zarejestruj("kolko", rysuj_na_pozycji)
zarzadca.zarejestruj("krzyzyk", rysuj_na_pozycji)

CZERWONY = pygame.color.THECOLORS['red']


def rysuj_obwodke(wielkosc_obszaru, surface):
    obwodka = pygame.Rect((0, 0), wielkosc_obszaru)
    obwodka.move_ip(*POCZATEK)
    pygame.draw.rect(surface, CZERWONY, obwodka, 1)


def _linia(poczatek, koniec, surface):
    pygame.draw.line(surface, CZERWONY, poczatek, koniec)

def rysuj_linie_poziome(wiersze, surface):
    pozx_pocz = POCZATEK[WIERSZ]
    pozx_koniec = pozx_pocz + wiersze * odleglosc
    y = POCZATEK[KOLUMNA]
    for p in range(1, wiersze):
        yn = y + p * odleglosc
        _linia((pozx_pocz, yn), (pozx_koniec, yn), surface)


def rysuj_linie_pionowe(kolumny, surface):
    pozy_pocz = POCZATEK[KOLUMNA]
    pozy_koniec = pozy_pocz + kolumny * odleglosc
    x = POCZATEK[WIERSZ]
    for p in range(1, kolumny):
        xn = x + p * odleglosc
        _linia((xn, pozy_pocz), (xn, pozy_koniec), surface)


def rysuj_siatke(plansza_rozmiar, surface):
    """ Rysuje plansze
    """
    wiersze, kolumny = plansza_rozmiar
    wielkosc_obszaru = (wiersze * odleglosc + 1,
                        kolumny * odleglosc + 1)
    rysuj_obwodke(wielkosc_obszaru, surface)
    rysuj_linie_poziome(wiersze, surface)
    rysuj_linie_pionowe(kolumny, surface)
    pygame.display.flip()


def czy_zatwierdzono_pozycje(events):
    wyj = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            wyj = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    return wyj


def odczyt_poz_myszy():
    zatwierdzono = False
    zegar = pygame.time.Clock()
    while not zatwierdzono:
        poz = pygame.mouse.get_pos()
        poz = [poz[1] - POCZATEK[1], poz[0] - POCZATEK[0]]
        poz_w = [x // (WIELKOSC + 1) for x in poz]
        zatwierdzono = czy_zatwierdzono_pozycje(pygame.event.get())
        zegar.tick(40)
    return siatka.Polozenie(poz_w)


def wyswietl_gracza(gracz, surface):
    WIELKOSC_FONT = 40
    POZYCJA = (400, 400)
    font = pygame.font.SysFont("", WIELKOSC_FONT)
    napis = font.render(gracz.nazwa, False, pygame.color.THECOLORS['green'])
    gumka = napis.get_rect().move(*POZYCJA)
    pygame.draw.rect(surface, pygame.color.THECOLORS['black'], gumka)
    pygame.display.flip()
    surface.blit(napis, POZYCJA)
    pygame.display.flip()

zarzadca.zarejestruj('wyswietl-gracza', wyswietl_gracza)

if __name__ == "__main__":
    import plansza
    surface = pygame.display.set_mode((800, 600))
    plansza_rozmiar = (15, 15)
    plansza = plansza.Plansza(surface, *plansza_rozmiar)
    rysuj_siatke(plansza_rozmiar, surface)
    symbol.Krzyzyk.postaw_na_planszy(plansza, (10, 10))
    symbol.Kolko.postaw_na_planszy(plansza, (13, 10))
    pygame.display.flip()
    while True:
        odczyt_poz_myszy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
