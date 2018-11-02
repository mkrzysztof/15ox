"""Gra"""
import pygame
import plansza
import zarzadca
import plansza_wyboru_mod as pwm
import time


def _czy_koniec(biezacy_gracz, remis):
    return (biezacy_gracz.wygrana or biezacy_gracz.przeciwnik.wygrana or remis)

def _pokaz_wygrana(biezacy_gracz, plansza):
    biezacy_gracz.ustaw_wygrana()
    zarzadca.rozeslij('pokaz-wygrana', False, biezacy_gracz, plansza.surface)

def _pokaz_remis(biezacy_gracz, plansza):
    remis = True
    zarzadca.rozeslij('pokaz-wygrana', remis, biezacy_gracz, plansza.surface)
    return remis

def _zdecyduj_o_koncu(biezacy_gracz, polozenie, plansza):
    """ zdecyduj no końcu dla bieżącego gracza na podstawie ostatniego 
    położenia dla danej planszy """
    remis = False
    if plansza.ma_uklad_wygrywajacy(polozenie):
        _pokaz_wygrana(biezacy_gracz, plansza)
        pwm.przerwano = True
        time.sleep(3)
    elif plansza.jest_zapelniona():
        remis = _pokaz_remis(biezacy_gracz, plansza)
        pwm.przerwano = True
        time.sleep(3)
    else:
        biezacy_gracz = biezacy_gracz.przeciwnik
    return biezacy_gracz, remis

def gra(pierwszy_gracz, drugi_gracz, plansza):
    """Główna procedura rozgrywki"""
    remis = False
    biezacy_gracz = pierwszy_gracz
    pwm.przerwano = False
    while not _czy_koniec(biezacy_gracz, remis) and not pwm.przerwano:
        zarzadca.rozeslij('wyswietl-gracza', biezacy_gracz, plansza.surface)
        polozenie = biezacy_gracz.postaw_symbol_na_planszy(plansza)
        biezacy_gracz, remis = _zdecyduj_o_koncu(biezacy_gracz, polozenie,
                                                plansza)
