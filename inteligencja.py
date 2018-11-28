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
    """ dodaje do wierczhołka element odpowiadający ruchowi na
    siatce nim etykietowany zwraca ten wierzcholek dla gracza"""
    wierzcholek_przeciwnika = stworz_wierzcholek_przeciwnika(wierzcholek, ruch)
    wierzcholek[ruch] = wierzcholek_przeciwnika
    return wierzcholek_przeciwnika

def wartosciuj_wierzcholek(wierzcholek, ostatni_ruch,
                           fun_wart=wartosciowanie.max_strony):
    a_siatka = wierzcholek.siatka
    gracz = wierzcholek.gracz
    wart = fun_wart(a_siatka, gracz, ostatni_ruch)
    wierzcholek.wartosc = wart

def dodaj_podwierzcholki(wierzcholek, stos, glebokosc=0,
                         fun_wolne=siatka.Siatka.wolne_pola):
    """ na podstawie zbioru wolnych pól na siatce dodaje
    do wierzcholka potomków reprezentujących następny ruch
    następnie umieść je na stosie"""
    siatka1 = wierzcholek.siatka
    wolne_pola = fun_wolne(siatka1)
    for ruch in wolne_pola:
        pod_wierzcholek = dodaj_ruch_na_siatce(wierzcholek, ruch)
        element = (pod_wierzcholek, ruch, glebokosc)
        stos.append(element)

def buduj_drzewo_stopnia(stan_siatki, gracz_aktywny, glebokosc):
    """buduj drzewo o głębokości glebokosc"""
    przeciwnik = gracz_aktywny.przeciwnik
    wierzch_wyj = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    stos = []
    licznik_stopnia = 0
    element = (wierzch_wyj, None, licznik_stopnia)
    stos.append(element)
    while stos:
        wierzcholek, ruch, licznik_stopnia = stos.pop()
        if licznik_stopnia < glebokosc:
            wartosciuj_wierzcholek(wierzcholek, ruch, FUN_WART)
            if licznik_stopnia == glebokosc - 1 and wierzcholek.wartosc is None:
                wierzcholek.wartosc = 0
            dodaj_podwierzcholki(wierzcholek, stos, licznik_stopnia + 1,
                                 siatka.Siatka.otoczenie)
            wierzcholek.siatka = None
    return wierzch_wyj

def klucz(x):
    return x[1]

def min_max(wierzcholek, gracz_aktywny):
    wartosc = wierzcholek.wartosc
    ruch = None
    fun_por = max if (wierzcholek.gracz != gracz_aktywny) else min
    if wartosc is None:
        wartosci = {}
        for ruch, dziecko in wierzcholek.items():
            _, dziecko.wartosc = min_max(dziecko, gracz_aktywny)
            wartosci[ruch] = dziecko.wartosc
        ruch, wartosc = fun_por(wartosci.items(), key=klucz)
        wierzcholek.wartosc = wartosc
    return (ruch, wartosc)
