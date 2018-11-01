import siatka
import plansza
import grafika
import ox15
import plansza_wyboru_wid as pww
import plansza_wyboru_mod as pwm
import pygame
import sys

ROZMIAR = (800, 600)
_kolor_czarny = pygame.color.THECOLORS['black']

def _obsloz_zamkniecie(events):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)

def _wybierz_opcje():
    events = pygame.event.get()
    pww.obsluz_przyciski_rozm(events)
    pww.obsluz_przyciski_ile(events)
    pww.obsloz_OK(events, pww.PRZYCISK_OK)
    _obsloz_zamkniecie(events)

def _przygotuj_formatki(surface):
    pww.utworz_przyciski_rozm(surface)
    pww.utworz_przyciski_ile(surface)
    pww.wyswietl_OK(surface)

def _uruchom_gre(surface):
    plansza_gry = plansza.Plansza(surface, *pwm.PLANSZA_ROZMIAR)
    siatka.WYGRYWAJACYCH = pwm.WYGRYWAJACYCH
    grafika.rysuj_siatke(pwm.PLANSZA_ROZMIAR, surface)
    ox15.gra(pwm.GRACZ1, pwm.GRACZ2, plansza_gry)

def _wybierz_opcje_gry(surface):
    surface.fill(_kolor_czarny)
    _przygotuj_formatki(surface)
    while not pwm.zatwierdzono_wybor:
        _wybierz_opcje()
    surface.fill(_kolor_czarny)
    pygame.display.flip()

def start_gry(surface):
    _wybierz_opcje_gry(surface)
    _uruchom_gre(surface)
    pwm.zatwierdzono_wybor = False


if __name__ == "__main__":
    surface = pygame.display.set_mode(ROZMIAR)
    while True:
        start_gry(surface)
