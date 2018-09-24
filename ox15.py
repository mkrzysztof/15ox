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


def gra(pierwszy_gracz, drugi_gracz, plansza):
    """Główna procedura rozgrywki"""
    # dopuki któryś z graczy nie wygra lub jest remis:\
    # bieżący gracz stawia swój symbol na wolnym polu planszsy\
    # jeżeli wykryrto układ wygrywający zgłoś wygraną bieżącego gracza\
    # w pp jeśli plansza zapełniona zgłoś remis\
    # w pp zmień bieżącego gracza
    remis = False
    biezacy_gracz = pierwszy_gracz
    while not (pierwszy_gracz.wygrana or drugi_gracz.wygrana or remis):
        zarzadca.rozeslij('wyswietl-gracza', biezacy_gracz, plansza.surface)
        polozenie = biezacy_gracz.postaw_symbol_na_planszy(plansza)
        if plansza.ma_uklad_wygrywajacy(polozenie):
            biezacy_gracz.ustaw_wygrana()
            print(plansza.pola)
        elif plansza.jest_zapelniona():
            remis = True
            print("Remis")
        else:
            biezacy_gracz = biezacy_gracz.przeciwnik

if __name__ == "__main__":
    SURFACE = pygame.display.set_mode((800, 600))
    pwm.wybierz_xo()
    siatka.WYGRYWAJACYCH = pwm.WYGRYWAJACYCH
    PLANSZA = plansza.Plansza(SURFACE, *pwm.PLANSZA_ROZMIAR)
    grafika.rysuj_siatke(pwm.PLANSZA_ROZMIAR, SURFACE)
    gra(pwm.GRACZ1, pwm.GRACZ2, PLANSZA)
