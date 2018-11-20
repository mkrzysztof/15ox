""" zawiera funkcje oceniające sytuacje w zależności od sytuacji na
siatce, aktywnego gracza i jego ostatniego ruchu"""

import siatka

def klasyczne_plus_minus(siatka, gracz, ostatni_ruch):
    """ gracz.mnoznik -- gracz wygrywa
    0 -- remis"""
    wyj = None
    if siatka.jest_zapelniona():
        print("xxxx")
        wyj = 0
    elif siatka.ma_uklad_wygrywajacy(ostatni_ruch):
        wyj = gracz.mnoznik
    return wyj


def max_strony(siatka, gracz, ostatni_ruch):
    """oblicz liczbę symboli dla każdej z 4-ech stron, weź największą
    z nich, uzyskany wynik przemnóz przez +1 lu b -1 w zależności od
    gracza """
    pass
