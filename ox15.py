"""Gra"""
import pygame
import siatka
import plansza
import grafika
import zarzadca
import plansza_koncowa
import plansza_wyboru_mod as pwm
from monitoring import pokaz_wywolanie
import time


def czy_koniec(biezacy_gracz, remis):
    return biezacy_gracz.wygrana or biezacy_gracz.przeciwnik.wygrana or remis

def pokaz_wygrana(biezacy_gracz, plansza_gry):
    biezacy_gracz.ustaw_wygrana()
    print(plansza_gry.pola)
    zarzadca.rozeslij('pokaz-wygrana', False, biezacy_gracz,
                      plansza_gry.surface)

def pokaz_remis(biezacy_gracz, plansza_gry):
    remis = True
    print("Remis")
    zarzadca.rozeslij('pokaz-wygrana', remis, biezacy_gracz,
                      plansza_gry.surface)
    return remis

def zdecyduj_o_koncu(biezacy_gracz, polozenie, plansza_gry):
    """zdecyduj no końcu dla bieżącego gracza na podstawie ostatniego
    położenia dla danej planszy """
    remis = False
    if plansza_gry.ma_uklad_wygrywajacy(polozenie):
        pokaz_wygrana(biezacy_gracz, plansza_gry)
    elif plansza_gry.jest_zapelniona():
        remis = pokaz_remis(biezacy_gracz, plansza_gry)
    else:
        biezacy_gracz = biezacy_gracz.przeciwnik
    return biezacy_gracz, remis

def gra(pierwszy_gracz, plansza_gry):
    """Główna procedura rozgrywki"""
    remis = False
    biezacy_gracz = pierwszy_gracz
    while not czy_koniec(biezacy_gracz, remis):
        zarzadca.rozeslij('wyswietl-gracza', biezacy_gracz,
                          plansza_gry.surface)
        polozenie = biezacy_gracz.postaw_symbol_na_planszy(plansza_gry)
        biezacy_gracz, remis = zdecyduj_o_koncu(biezacy_gracz, polozenie,
                                                plansza_gry)
    # pauza
    time.sleep(5.5)

zarzadca.zarejestruj('pokaz-wygrana', plansza_koncowa.pokaz_wygrana)
if __name__ == "__main__":
    SURFACE = pygame.display.set_mode((800, 600))
    pwm.wybierz_xo()
    siatka.WYGRYWAJACYCH = pwm.WYGRYWAJACYCH
    PLANSZA = plansza.Plansza(SURFACE, *pwm.PLANSZA_ROZMIAR)
    grafika.rysuj_siatke(pwm.PLANSZA_ROZMIAR, SURFACE)
    gra(pwm.GRACZ1, pwm.GRACZ2, PLANSZA)
