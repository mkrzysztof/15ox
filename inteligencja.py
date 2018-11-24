import drzewo
import wartosciowanie

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
                           fun_wart=wartosciowanie.klasyczne_plus_minus):
    a_siatka = wierzcholek.siatka
    gracz = wierzcholek.gracz
    wart = fun_wart(a_siatka, gracz, ostatni_ruch)
    wierzcholek.wartosc = wart

def dodaj_podwierzcholki(wierzcholek, stos, stopien=0):
    """ na podstawie zbioru wolnych pól na siatce dodaje
    do wierzcholka potomków reprezentujących następny ruch
    następnie umieść je na stosie"""
    wolne_pola = wierzcholek.siatka.wolne_pola()
    for ruch in wolne_pola:
        pod_wierzcholek = dodaj_ruch_na_siatce(wierzcholek, ruch)
        element = (pod_wierzcholek, ruch, stopien)
        stos.append(element)

def buduj_drzewo_stopnia(stan_siatki, gracz_aktywny, stopien):
    """buduj drzewo o głębokości stopien"""
    przeciwnik = gracz_aktywny.przeciwnik
    wierzch_wyj = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    stos = []
    licznik_stopnia = 0
    element = (wierzch_wyj, None, licznik_stopnia)
    stos.append(element)
    while stos:
        wierzcholek, ruch, licznik_stopnia = stos.pop()
        if licznik_stopnia < stopien:
            wartosciuj_wierzcholek(wierzcholek, ruch)
            if licznik_stopnia == stopien - 1 and wierzcholek.wartosc is None:
                wierzcholek.wartosc = 0
            dodaj_podwierzcholki(wierzcholek, stos, licznik_stopnia + 1)
            wierzcholek.siatka = None
    return wierzch_wyj

def buduj_drzewo(stan_siatki, gracz_aktywny):
    przeciwnik = gracz_aktywny.przeciwnik
    wierzch_wyj = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    stos = []
    element = (wierzch_wyj, None)
    stos.append(element)
    while stos:
        wierzcholek, ruch = stos.pop()
        wartosciuj_wierzcholek(wierzcholek, ruch, wierzcholek,max_strony)
        dodaj_podwierzcholki(wierzcholek, stos)
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
