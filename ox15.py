"""Gra"""
import pygame
import plansza
import symbol
import gracz
import grafika
import gracz_komputer
from monitoring import pokaz_wywolanie

def gra(pierwszy_gracz, drugi_gracz, plansza):
    """Główna procedura rozgrywki"""
    # dopuki któryś z graczy nie wygra lub jest remis:\
    # bieżący gracz stawia swój symbol na wolnym polu planszsy\
    # jeżeli wykryrto układ wygrywający zgłoś wygraną bieżącego gracza\
    # w pp jeśli plansza zapełniona zgłoś remis\
    # w pp zmień bieżącego gracza
    remis = False
    gracze = (pierwszy_gracz, drugi_gracz)
    num_gracza = 0
    while not (pierwszy_gracz.wygrana or drugi_gracz.wygrana or remis):
        biezacy_gracz = gracze[num_gracza]
        polozenie = biezacy_gracz.postaw_symbol_na_planszy(plansza)
        if plansza.ma_uklad_wygrywajacy(polozenie):
            biezacy_gracz.ustaw_wygrana()
        elif plansza.jest_zapelniona():
            remis = True
            print("Remis")
        else:
            num_gracza = (num_gracza + 1) % 2

if __name__ == "__main__":
    SURFACE = pygame.display.set_mode((800, 600))
    PLANSZA = plansza.Plansza(SURFACE)
    PLANSZA_ROZMIAR = (15, 15)
    grafika.rysuj_siatke(PLANSZA_ROZMIAR, SURFACE)
    GRACZ1 = gracz.GraczCzlowiek(symbol.Kolko)
    GRACZ2 = gracz_komputer.GraczKomputer(symbol.Krzyzyk)
    GRACZ1.przeciwnik = GRACZ2
    GRACZ2.przeciwnik = GRACZ1
    GRACZ2.mnoznik = -1
    GRACZ2.mnoznik = 1
    gra(GRACZ1, GRACZ2, PLANSZA)
