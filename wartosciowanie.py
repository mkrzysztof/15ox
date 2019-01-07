""" zawiera funkcje oceniające sytuacje w zależności od sytuacji na
siatce, aktywnego gracza i jego ostatniego ruchu"""

import siatka
import parametry


def klasyczne_plus_minus(stan_gry, faza):
    """stan_gry słownik o kluczach: siatka, ostatni_ruch
    faza faza gry ALFA lub BETA"""
    wyj = 0
    biez_siatka = stan_gry.siatka
    ostatni_ruch = stan_gry.ostatni_ruch
    if biez_siatka.jest_zapelniona():
        wyj = 0
    elif biez_siatka.ma_uklad_wygrywajacy(ostatni_ruch):
        wyj = parametry.mnoznik(faza)
    return wyj


def max_strony(stan_gry, faza):
    """oblicz liczbę symboli dla każdej z 4-ech stron, weź największą
    z nich, uzyskany wynik przemnóz przez +1 lub -1 w zależności od
    gracza """
    biez_siatka = stan_gry.siatka
    ostatni_ruch = stan_gry.ostatni_ruch
    if not ostatni_ruch:
        return None
    lista_ilosci = []
    strony = {siatka.POZIOM, siatka.PION, siatka.UKOS_LEWY, siatka.UKOS_PRAWY}
    for strona in strony:
        ile = biez_siatka.policz_symbol_strona(ostatni_ruch, strona)
        lista_ilosci.append(ile)
        mnoznik = parametry.mnoznik(faza)
    return max(lista_ilosci) * mnoznik
