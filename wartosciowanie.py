""" zawiera funkcje oceniające sytuacje w zależności od sytuacji na
siatce, aktywnego gracza i jego ostatniego ruchu"""

import enum
import siatka
import gracz_komputer

    
def klasyczne_plus_minus(stan_gry, gracz):
    """stan_gry słownik o kluczach: siatka, ostatni_ruch
    gracz in {"CZLOWIEK", "KOMPUTER"}"""
    wyj = 0
    biez_siatka = stan_gry["siatka"]
    ostatni_ruch = stan_gry["ostatni_ruch"]
    if biez_siatka.jest_zapelniona():
        wyj = 0
    elif biez_siatka.ma_uklad_wygrywajacy(ostatni_ruch):
        wyj = gracz_komputer.Gracze_Parametry[gracz]["mnoznik"]
    return wyj


def max_strony(stan_gry, gracz):
    """oblicz liczbę symboli dla każdej z 4-ech stron, weź największą
    z nich, uzyskany wynik przemnóz przez +1 lub -1 w zależności od
    gracza """
    biez_siatka = stan_gry["siatka"]
    ostatni_ruch = stan_gry["ostatni_ruch"]
    if not ostatni_ruch:
        return None
    lista_ilosci = []
    strony = {siatka.POZIOM, siatka.PION, siatka.UKOS_LEWY, siatka.UKOS_PRAWY}
    for strona in strony:
        ile = biez_siatka.policz_symbol_strona(ostatni_ruch, strona)
        lista_ilosci.append(ile)
        mnoznik = gracz_komputer.Gracze_Parametry[gracz]["mnoznik"]
    return max(lista_ilosci) * mnoznik
