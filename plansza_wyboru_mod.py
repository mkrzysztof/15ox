"""zawiera ustawienia gry"""
import gracz
import symbole
import gracz_komputer

PLANSZA_ROZMIAR = (15, 15)
WYGRYWAJACYCH = 3
GRACZ1 = gracz.GraczCzlowiek(symbole.Kolko, "Gracz1")
GRACZ2 = gracz.GraczCzlowiek(symbole.Krzyzyk, "Gracz2")
GRACZ1.przeciwnik = GRACZ2
GRACZ2.przeciwnik = GRACZ1

zatwierdzono_wybor = False

def wybierz_xo():
    """klasyczna gra w kółko i krzyżyk na planszy 3x3"""
    global PLANSZA_ROZMIAR, WYGRYWAJACYCH
    PLANSZA_ROZMIAR = (3, 3)
    WYGRYWAJACYCH = 3

def wybierz_5():
    """gra 5 symbolei w jednej linii"""
    global PLANSZA_ROZMIAR, WYGRYWAJACYCH
    WYGRYWAJACYCH = 5
    PLANSZA_ROZMIAR = (10, 10)

def wybierz_10x10():
    """wybierz planszę 10x10"""
    global PLANSZA_ROZMIAR, WYGRYWAJACYCH
    WYGRYWAJACYCH = 5
    PLANSZA_ROZMIAR = (10, 10)

def wybierz_15x15():
    """wybierz planszę 15x15"""
    global PLANSZA_ROZMIAR, WYGRYWAJACYCH
    WYGRYWAJACYCH = 5
    PLANSZA_ROZMIAR = (15, 15)

def wybierz_gracz_gracz():
    global GRACZ1, GRACZ2
    GRACZ1 = gracz.GraczCzlowiek(symbole.Kolko, "Gracz1")
    GRACZ2 = gracz.GraczCzlowiek(symbole.Krzyzyk, "Gracz2")
    GRACZ1.przeciwnik = GRACZ2
    GRACZ2.przeciwnik = GRACZ1

def wybierz_gracz_komputer():
    global GRACZ1, GRACZ2
    GRACZ1 = gracz.GraczCzlowiek(symbole.Kolko, "Gracz1")
    GRACZ2 = gracz_komputer.GraczKomputer(symbole.Krzyzyk, "Gracz2")
    GRACZ1.przeciwnik = GRACZ2
    GRACZ2.przeciwnik = GRACZ1

def wybierz_komputer_gracz():
    global GRACZ1, GRACZ2
    GRACZ1 = gracz_komputer.GraczKomputer(symbole.Kolko, "Gracz1")
    GRACZ2 = gracz.GraczCzlowiek(symbole.Krzyzyk, "Gracz2")
    GRACZ1.przeciwnik = GRACZ2
    GRACZ2.przeciwnik = GRACZ1
