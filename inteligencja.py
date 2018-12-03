"""odpowiada za inteligencję, głównie budowa i ocena drzewa gry"""
import drzewo

import siatka


def _stworz_wierzcholek_przeciwnika(wierzcholek, ruch):
    """stwórz wierzcholek odpowiadający temu jak przeciwik wykona ruch"""
    przeciwnik = wierzcholek.gracz.przeciwnik
    nastepna_siatka = wierzcholek.siatka.copy()
    nastepna_siatka[ruch] = przeciwnik.symbol
    return drzewo.Wierzcholek(nastepna_siatka, przeciwnik)

def _dodaj_ruch_na_siatce(wierzcholek, ruch):
    """ dodaje do wierzchołka element odpowiadający ruchowi na
    siatce nim etykietowany zwraca ten wierzcholek dla gracza"""
    wierzcholek_przeciwnika = _stworz_wierzcholek_przeciwnika(wierzcholek,
                                                              ruch)
    wierzcholek[ruch] = wierzcholek_przeciwnika
    return wierzcholek_przeciwnika

def _wartosciuj_wierzcholek(wierzcholek, ostatni_ruch, fun_wart):
    """oceń wierzchołek na podstawie sytuacji i ostatnio wykonanego ruchu"""
    a_siatka = wierzcholek.siatka
    gracz = wierzcholek.gracz
    wart = fun_wart(a_siatka, gracz, ostatni_ruch)
    return wart

def _dodaj_podwierzcholki(wierzcholek, stos, glebokosc, fun_wolne):
    """ na podstawie zbioru wolnych pól na siatce dodaje
    do wierzcholka potomków reprezentujących następny ruch
    następnie umieść je na stosie"""
    siatka1 = wierzcholek.siatka
    wolne_pola = fun_wolne(siatka1)
    for ruch in wolne_pola:
        pod_wierzcholek = _dodaj_ruch_na_siatce(wierzcholek, ruch)
        element = (pod_wierzcholek, ruch, glebokosc)
        stos.append(element)

def _ocen_lub_dodaj(wierzcholek, licznik_stopnia, fun_wolne, fun_wart,
                   ostatni_ruch, stos):
    """w zależności od sytuacji oceń wierzchołek, lub dodaj do niego
    podwierzchołki, wkładając je na stos, wolne wierzchołki określa funkcja
    fun_wolne, dla ostatnio wykonanego ruchu"""
    siatka_wierzch = wierzcholek.siatka
    ocena = _wartosciuj_wierzcholek(wierzcholek, ostatni_ruch, fun_wart)
    if siatka_wierzch.jest_zapelniona():
        wierzcholek.wartosc = 0
    elif siatka_wierzch.ma_uklad_wygrywajacy(ostatni_ruch):
        wierzcholek.wartosc = ocena
    else:
        _dodaj_podwierzcholki(wierzcholek, stos, licznik_stopnia + 1,
                              fun_wolne)

def _stworz_korzen(stan_siatki, gracz_aktywny, stos):
    """stwórz korzeń drzewa i poślij jego "parametry" na stos
    zwróć utworzony wierzchołek"""
    przeciwnik = gracz_aktywny.przeciwnik
    wierzch_wyj = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    ruch = None
    licznik_stopnia = 0
    element = (wierzch_wyj, ruch, licznik_stopnia)
    stos.append(element)
    return wierzch_wyj

def buduj_drzewo_stopnia(stan_siatki, gracz_aktywny, glebokosc, fun_wolne,
                         fun_wart):
    """buduj drzewo o zadanej głębokości. Korzeń zawiera sytuację po ostatnim 
    ruchu przeciwnika.W przypadku początku gry jest pusta siatka """
    stos = []
    wierzch_wyj = _stworz_korzen(stan_siatki, gracz_aktywny, stos)
    while stos:
        wierzcholek, ruch, licznik_stopnia = stos.pop()
        if licznik_stopnia < glebokosc:
            _ocen_lub_dodaj(wierzcholek, licznik_stopnia, fun_wolne, fun_wart,
                           ruch, stos)
        else:
            ocena = _wartosciuj_wierzcholek(wierzcholek, ruch, fun_wart)
            wierzcholek.wartosc = ocena
        wierzcholek.siatka = None
    return wierzch_wyj

def _klucz(lst):
    return lst[1]

def min_max(wierzcholek, gracz_aktywny):
    """algorytm min-max na drzewie o wierzchołku wierzcholek"""
    wartosc = wierzcholek.wartosc
    ruch = None
    fun_por = max if (wierzcholek.gracz != gracz_aktywny) else min
    if wierzcholek.items():
        wartosci = {}
        for ruch, dziecko in wierzcholek.items():
            _, dziecko.wartosc = min_max(dziecko, gracz_aktywny)
            wartosci[ruch] = dziecko.wartosc
        ruch, wartosc = fun_por(wartosci.items(), key=_klucz)
        wierzcholek.wartosc = wartosc
    return (ruch, wartosc)
