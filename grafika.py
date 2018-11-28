""" obsługa grafiki. Rysowanie planszy/siatki gry. wyświetlanie informacji
o grze"""

import sys
import pygame
import siatka
import symbole
import zarzadca

# stałe
WIELKOSC = 20  # liczba pixeli przypadających na komórkę
ODLEGLOSC = WIELKOSC + 1
POCZATEK = (50, 50)
WIERSZ = 0
KOLUMNA = 1


pygame.init()


class SymboleGraf:
    """graficzna reprezentacja x lub o"""

    def __init__(self):
        self.font = pygame.font.SysFont("", 30)
        self.sym = None


class Kolko_graf(SymboleGraf):
    def __init__(self):
        super().__init__()
        self.sym = self.font.render('o', False, (0, 255, 0))
        self.sym = pygame.transform.scale(self.sym, (WIELKOSC, WIELKOSC))


class Krzyzyk_graf(SymboleGraf):
    def __init__(self):
        super().__init__()
        self.sym = self.font.render('x', False, (0, 255, 0))
        self.sym = pygame.transform.scale(self.sym, (WIELKOSC, WIELKOSC))


class Puste_graf(SymboleGraf):
    pass


REPREZENTACJA = {symbole.Puste: Puste_graf(), symbole.Kolko: Kolko_graf(),
                 symbole.Krzyzyk: Krzyzyk_graf()}


def rysuj_na_pozycji(symbol, pozycja, surface):
    """rysuj reprezentację symbol na surface na pozycji
    (współrzędne ekranowe)"""
    poz_x = POCZATEK[KOLUMNA] + pozycja[KOLUMNA] * ODLEGLOSC
    poz_y = POCZATEK[WIERSZ] + pozycja[WIERSZ] * ODLEGLOSC
    surface.blit(REPREZENTACJA[symbol].sym, (poz_x, poz_y))
    pygame.display.flip()

zarzadca.zarejestruj("kolko", rysuj_na_pozycji)
zarzadca.zarejestruj("krzyzyk", rysuj_na_pozycji)

CZERWONY = pygame.color.THECOLORS['red']


def _rysuj_obwodke(wielkosc_obszaru, surface):
    obwodka = pygame.Rect((0, 0), wielkosc_obszaru)
    obwodka.move_ip(*POCZATEK)
    pygame.draw.rect(surface, CZERWONY, obwodka, 1)


def _linia(poczatek, koniec, surface):
    pygame.draw.line(surface, CZERWONY, poczatek, koniec)

def _rysuj_linie_poziome(wiersze, surface):
    pozx_pocz = POCZATEK[WIERSZ]
    pozx_koniec = pozx_pocz + wiersze * ODLEGLOSC
    pozy_pocz = POCZATEK[KOLUMNA]
    for nr_wier in range(1, wiersze):
        pozy_koniec = pozy_pocz + nr_wier * ODLEGLOSC
        _linia((pozx_pocz, pozy_koniec), (pozx_koniec, pozy_koniec), surface)


def _rysuj_linie_pionowe(kolumny, surface):
    pozy_pocz = POCZATEK[KOLUMNA]
    pozy_koniec = pozy_pocz + kolumny * ODLEGLOSC
    pozx_pocz = POCZATEK[WIERSZ]
    for nr_kol in range(1, kolumny):
        pozx_koniec = pozx_pocz + nr_kol * ODLEGLOSC
        _linia((pozx_koniec, pozy_pocz), (pozx_koniec, pozy_koniec), surface)


def rysuj_siatke(plansza_rozmiar, surface):
    """ Rysuje plansze
    """
    wiersze, kolumny = plansza_rozmiar
    wielkosc_obszaru = (wiersze * ODLEGLOSC + 1,
                        kolumny * ODLEGLOSC + 1)
    _rysuj_obwodke(wielkosc_obszaru, surface)
    _rysuj_linie_poziome(wiersze, surface)
    _rysuj_linie_pionowe(kolumny, surface)
    pygame.display.flip()


def _czy_zatwierdzono_pozycje(events):
    wyj = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            wyj = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    return wyj


def odczyt_poz_myszy():
    """odczytuje pozycję myszy na siatce"""
    zatwierdzono = False
    zegar = pygame.time.Clock()
    while not zatwierdzono:
        poz = pygame.mouse.get_pos()
        poz = [poz[1] - POCZATEK[1], poz[0] - POCZATEK[0]]
        poz_w = [x // (WIELKOSC + 1) for x in poz]
        zatwierdzono = _czy_zatwierdzono_pozycje(pygame.event.get())
        zegar.tick(40)
    return siatka.Polozenie(poz_w)


def wyswietl_gracza(gracz, surface):
    """wyświetl informacje otym że gra gracz"""
    wielkosc_font = 40
    pozycja = (400, 400)
    font = pygame.font.SysFont("", wielkosc_font)
    napis = font.render(gracz.nazwa, False, pygame.color.THECOLORS['green'])
    gumka = napis.get_rect().move(*pozycja)
    pygame.draw.rect(surface, pygame.color.THECOLORS['black'], gumka)
    pygame.display.flip()
    surface.blit(napis, pozycja)
    pygame.display.flip()

zarzadca.zarejestruj('wyswietl-gracza', wyswietl_gracza)
