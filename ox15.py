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


def gra(pierwszy_gracz, drugi_gracz, plansza):
    """Główna procedura rozgrywki"""
    # dopuki któryś z graczy nie wygra lub jest remis:\
    # bieżący gracz stawia swój symbol na wolnym polu planszsy\
    # jeżeli wykryrto układ wygrywający zgłoś wygraną bieżącego gracza\
    # w pp jeśli plansza zapełniona zgłoś remis\
    # w pp zmień bieżącego gracza
    remis = False
    biezacy_gracz = pierwszy_gracz
    def zdecyduj_o_koncu():
        nonlocal biezacy_gracz, remis
        if plansza.ma_uklad_wygrywajacy(polozenie):
            biezacy_gracz.ustaw_wygrana()
            print(plansza.pola)
            zarzadca.rozeslij('pokaz-wygrana', remis, biezacy_gracz,
                              plansza.surface)
        elif plansza.jest_zapelniona():
            remis = True
            print("Remis")
            zarzadca.rozeslij('pokaz-wygrana', remis, biezacy_gracz,
                              plansza.surface)
        else:
            biezacy_gracz = biezacy_gracz.przeciwnik

    def czy_koniec():
        return (pierwszy_gracz.wygrana or drugi_gracz.wygrana or remis)
            
    while not czy_koniec():
        zarzadca.rozeslij('wyswietl-gracza', biezacy_gracz, plansza.surface)
        polozenie = biezacy_gracz.postaw_symbol_na_planszy(plansza)
        zdecyduj_o_koncu()
    # pauza
    time.sleep(5.5)

if __name__ == "__main__":
    SURFACE = pygame.display.set_mode((800, 600))
    pwm.wybierz_xo()
    siatka.WYGRYWAJACYCH = pwm.WYGRYWAJACYCH
    PLANSZA = plansza.Plansza(SURFACE, *pwm.PLANSZA_ROZMIAR)
    grafika.rysuj_siatke(pwm.PLANSZA_ROZMIAR, SURFACE)
    gra(pwm.GRACZ1, pwm.GRACZ2, PLANSZA)
