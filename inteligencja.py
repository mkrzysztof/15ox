"""odpowiada za inteligencję, głównie budowa i ocena drzewa gry"""
import drzewo
import wartosciowanie
import siatka

FUN_WART = wartosciowanie.klasyczne_plus_minus

def stworz_wierzcholek_przeciwnika(wierzcholek, ruch):
    """stwórz wierzcholek odpowiadający temu jak przeciwik wykona ruch"""
    przeciwnik = wierzcholek.gracz.przeciwnik
    nastepna_siatka = wierzcholek.siatka.copy()
    nastepna_siatka[ruch] = przeciwnik.symbol
    return drzewo.Wierzcholek(nastepna_siatka, przeciwnik)

def dodaj_ruch_na_siatce(wierzcholek, ruch):
    """ dodaje do wierzchołka element odpowiadający ruchowi na
    siatce nim etykietowany zwraca ten wierzcholek dla gracza"""
    wierzcholek_przeciwnika = stworz_wierzcholek_przeciwnika(wierzcholek, ruch)
    wierzcholek[ruch] = wierzcholek_przeciwnika
    return wierzcholek_przeciwnika

def wartosciuj_wierzcholek(wierzcholek, ostatni_ruch,
                           fun_wart=wartosciowanie.max_strony):
    """oceń wierzchołek na podstawie sytuacji i ostatnio wykonanego ruchu"""
    a_siatka = wierzcholek.siatka
    gracz = wierzcholek.gracz
    wart = fun_wart(a_siatka, gracz, ostatni_ruch)
    return wart

def dodaj_podwierzcholki(wierzcholek, stos, glebokosc=0,
                         fun_wolne=siatka.wolne_pola):
    """ na podstawie zbioru wolnych pól na siatce dodaje
    do wierzcholka potomków reprezentujących następny ruch
    następnie umieść je na stosie"""
    siatka1 = wierzcholek.siatka
    wolne_pola = fun_wolne(siatka1)
    for ruch in wolne_pola:
        pod_wierzcholek = dodaj_ruch_na_siatce(wierzcholek, ruch)
        element = (pod_wierzcholek, ruch, glebokosc)
        stos.append(element)

def buduj_drzewo_stopnia(stan_siatki, gracz_aktywny, glebokosc, fun_wolne):
    """buduj drzewo o zadanej głębokości. Korzeń zawiera sytuację
    po ostatnim ruchu przeciwnika
    W przypadku początku gry jest pusta siatka """
    stos = []
    przeciwnik = gracz_aktywny.przeciwnik
    wierzch_wyj = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    licznik_stopnia = 0
    ruch = None
    element = (wierzch_wyj, ruch, licznik_stopnia)
    stos.append(element)
    while stos:
        wierzcholek, ruch, licznik_stopnia = stos.pop()
        ocena = wartosciuj_wierzcholek(wierzcholek, ruch, FUN_WART)
        if licznik_stopnia < glebokosc:
            if wierzcholek.siatka.jest_zapelniona():
                wierzcholek.wartosc = 0
            elif wierzcholek.siatka.ma_uklad_wygrywajacy(ruch):
                wierzcholek.wartosc = ocena
            else:
                dodaj_podwierzcholki(wierzcholek, stos, licznik_stopnia + 1,
                                     fun_wolne)
        else:
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
