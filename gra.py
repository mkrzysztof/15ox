import siatka
import plansza
import grafika
import ox15
import plansza_wyboru_wid as pww
import plansza_wyboru_mod as pwm
import pygame
import sys

def obsloz_zamkniecie(events):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)

def wybierz_opcje():
    events = pygame.event.get()
    pww.obsluz_przyciski(events, pww.PRZYCISKI_ZMIAN)
    pww.obsluz_przyciski(events, pww.PRZYCISKI_KTO_GRA)
    pww.obsloz_OK(events, pww.PRZYCISK_OK)
    obsloz_zamkniecie(events)

def przygotuj_formatki(surface):
    pww.utworz_przyciski_rozm(surface)
    pww.dodaj_napisy_rozm(surface)
    pww.wyswietl_OK(surface)
    pww.utworz_przyciski_ile(surface)
    pww.dodaj_napisy_ile(surface)

def uruchom_gre(surface):
    plansza_gry = plansza.Plansza(surface, *pwm.PLANSZA_ROZMIAR)
    siatka.WYGRYWAJACYCH = pwm.WYGRYWAJACYCH
    grafika.rysuj_siatke(pwm.PLANSZA_ROZMIAR, surface)
    ox15.gra(pwm.GRACZ1, pwm.GRACZ2, plansza_gry)

def pokaz_wybory(surface):
    kolor_czarny = pygame.color.THECOLORS['black']
    surface.fill(kolor_czarny)
    przygotuj_formatki(surface)
    while not pwm.zatwierdzono_wybor:
        wybierz_opcje()
    surface.fill(kolor_czarny)
    pygame.display.flip()
    uruchom_gre(surface)
    pwm.zatwierdzono_wybor = False


if __name__ == "__main__":
    surface = pygame.display.set_mode(pww.ROZMIAR)
    while True:
        pokaz_wybory(surface)
