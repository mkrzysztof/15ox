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

def pokaz_wybory():
    surface = pygame.display.set_mode(pww.ROZMIAR)
    pww.utworz_przyciski_rozm(surface)
    pww.dodaj_napisy_rozm(surface)
    pww.wyswietl_OK(surface)
    pww.utworz_przyciski_ile(surface)
    pww.dodaj_napisy_ile(surface)
    while not pwm.zatwierdzono_wybor:
        events = pygame.event.get()
        pww.obsluz_przyciski_rozm(events, pww.PRZYCISKI_ZMIAN)
        pww.obsluz_przyciski_ile(events, pww.PRZYCISKI_KTO_GRA)
        pww.obsloz_OK(events, pww.PRZYCISK_OK)
        obsloz_zamkniecie(events)
    surface.fill(pygame.color.THECOLORS['black'])
    pygame.display.flip()
    plansza_gry = plansza.Plansza(surface, *pwm.PLANSZA_ROZMIAR)
    siatka.WYGRYWAJACYCH = pwm.WYGRYWAJACYCH
    grafika.rysuj_siatke(pwm.PLANSZA_ROZMIAR, surface)
    ox15.gra(pwm.GRACZ1, pwm.GRACZ2, plansza_gry)


if __name__ == "__main__":
    pokaz_wybory()
