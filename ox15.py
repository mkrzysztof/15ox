"""Gra"""
import pygame
import plansza
import symbol
import gracz
import grafika
import zarzadca

def pokaz_wywolanie(fun):
    """raportuje wuwołanie funkcjii do adnotacji"""
    def __opakowanie(*args, **kwds):
        print('wywołuję: ', fun.__name__)
        return fun(*args, **kwds)
    return __opakowanie

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
        zarzadca.rozeslij('wyswietl-gracza', biezacy_gracz, plansza.surface)
        polozenie = biezacy_gracz.postaw_symbol_na_planszy(plansza)
        if plansza.ma_uklad_wygrywajacy(polozenie):
            biezacy_gracz.ustaw_wygrana()
        elif plansza.jest_zapelniona():
            remis = True
        else:
            num_gracza = (num_gracza + 1) % 2

if __name__ == "__main__":
    SURFACE = pygame.display.set_mode((800, 600))
    PLANSZA = plansza.Plansza(SURFACE)
    PLANSZA_ROZMIAR = (15, 15)
    grafika.rysuj_siatke(PLANSZA_ROZMIAR, SURFACE)
    GRACZ1 = gracz.GraczCzlowiek(symbol.Kolko, "Gracz 1")
    GRACZ2 = gracz.GraczCzlowiek(symbol.Krzyzyk, "Gracz 2")
    GRACZ1.przeciwnik = GRACZ2
    GRACZ2.przeciwnik = GRACZ1
    gra(GRACZ1, GRACZ2, PLANSZA)
