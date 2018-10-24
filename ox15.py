"""Gra"""
import pygame
import siatka
import plansza
import symbol
import gracz
import grafika
import zarzadca
import gracz_komputer
import plansza_wyboru_mod as pwm
from monitoring import pokaz_wywolanie
import plansza_koncowa
import time


def czy_koniec(biezacy_gracz, remis):
    return (biezacy_gracz.wygrana or biezacy_gracz.przeciwnik.wygrana or remis)

def pokaz_wygrana(biezacy_gracz, plansza):
    biezacy_gracz.ustaw_wygrana()
    print(plansza.pola)
    zarzadca.rozeslij('pokaz-wygrana', False, biezacy_gracz, plansza.surface)

def pokaz_remis(biezacy_gracz, plansza):
    remis = True
    print("Remis")
    zarzadca.rozeslij('pokaz-wygrana', remis, biezacy_gracz, plansza.surface)
    return remis

def zdecyduj_o_koncu(biezacy_gracz, polozenie, plansza):
    """ zdecyduj no końcu dla bieżącego gracza na podstawie ostatniego 
    położenia dla danej planszy """
    remis = False
    if plansza.ma_uklad_wygrywajacy(polozenie):
        pokaz_wygrana(biezacy_gracz, plansza)
    elif plansza.jest_zapelniona():
        remis = pokaz_remis(biezacy_gracz, plansza)
    else:
        biezacy_gracz = biezacy_gracz.przeciwnik
    return biezacy_gracz, remis

def gra(pierwszy_gracz, drugi_gracz, plansza):
    """Główna procedura rozgrywki"""
    remis = False
    biezacy_gracz = pierwszy_gracz        
    while not czy_koniec(biezacy_gracz, remis):
        zarzadca.rozeslij('wyswietl-gracza', biezacy_gracz, plansza.surface)
        polozenie = biezacy_gracz.postaw_symbol_na_planszy(plansza)
        biezacy_gracz, remis = zdecyduj_o_koncu(biezacy_gracz, polozenie,
                                                plansza)
    # pauza
    time.sleep(5.5)

if __name__ == "__main__":
    SURFACE = pygame.display.set_mode((800, 600))
    pwm.wybierz_xo()
    siatka.WYGRYWAJACYCH = pwm.WYGRYWAJACYCH
    PLANSZA = plansza.Plansza(SURFACE, *pwm.PLANSZA_ROZMIAR)
    grafika.rysuj_siatke(pwm.PLANSZA_ROZMIAR, SURFACE)
    gra(pwm.GRACZ1, pwm.GRACZ2, PLANSZA)
