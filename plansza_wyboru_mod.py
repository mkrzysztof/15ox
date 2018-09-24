"""zawiera ustawienia gry"""
import gracz
import symbol

PLANSZA_ROZMIAR = (15, 15)
WYGRYWAJACYCH = 3
GRACZ1 = gracz.GraczCzlowiek(symbol.Kolko, "Gracz1")
GRACZ2 = gracz.GraczCzlowiek(symbol.Krzyzyk, "Gracz2")
GRACZ1.przeciwnik = GRACZ2
GRACZ2.przeciwnik = GRACZ1

def wybierz_xo():
    """klasyczna gra w kółko i krzyżyk na planszy 3x3"""
    global PLANSZA_ROZMIAR
    PLANSZA_ROZMIAR = (3, 3)

def wybierz_5():
    """gra 5 symboli w jednej linii"""
    global PLANSZA_ROZMIAR, WYGRANYCH
    WYGRANYCH = 5
    PLANSZA_ROZMIAR = (10, 10)

def wybierz_10x10():
    """wybierz planszę 10x10"""
    pass

def wybierz_15x15():
    """wybierz planszę 15x15"""
    pass
