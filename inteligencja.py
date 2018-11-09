import drzewo
import siatka
import gracz


def dodaj_ruch_na_siatce(wierzcholek, siatka, ruch, gracz):
    """ dodaje do wierczhołka element odpowiadający ruchowi na 
    siatce nim etykietowany zwraca ten wierzcholek dla gracza"""
    nastepna_siatka = siatka.copy()
    przeciwnik = gracz.przeciwnik
    nastepna_siatka[ruch] = przeciwnik.symbol
    pod_wierzcholek = drzewo.Wierzcholek(nastepna_siatka, przeciwnik)
    wierzcholek.dodaj(ruch, pod_wierzcholek)
    return pod_wierzcholek

def buduj_drzewo(stan_siatki, gracz_aktywny):
    przeciwnik = gracz_aktywny.przeciwnik
    glebokosc = 0
    wierzch_wyj = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    stos = []
    element = (wierzch_wyj, None, glebokosc)
    stos.append(element)
    while len(stos) != 0:
        wierzcholek, ruch, glebokosc = stos.pop()
        glebokosc += 1
        siatka = wierzcholek.siatka.copy()
        gracz = wierzcholek.gracz
        wolne_pola = []
        if siatka.jest_zapelniona():
            wierzcholek.wartosc = 0
        elif ruch is not None:
            if siatka.ma_uklad_wygrywajacy(ruch):
                wierzcholek.wartosc = gracz.mnoznik
            else:
                wolne_pola = siatka.wolne_pola()
        else:
            wolne_pola = siatka.wolne_pola()
        for ruch in wolne_pola:
            pod_wierzcholek = dodaj_ruch_na_siatce(wierzcholek, siatka, ruch,
                                                   gracz)
            element = (pod_wierzcholek, ruch, glebokosc)
            stos.append(element)
        wierzcholek.siatka = None
    return wierzch_wyj

def klucz(x):
    return x[1]

def min_max(wierzcholek, gracz_aktywny):
    wartosc = wierzcholek.wartosc
    ruch = None
    fun_por = None
    if wierzcholek.gracz != gracz_aktywny:
        fun_por = max
    else:
        fun_por = min
    if wartosc is None:
        wartosci = {}
        for ruch in wierzcholek.keys():
            dziecko = wierzcholek.odczytaj(ruch)
            dziecko.wartosc = min_max(dziecko, gracz_aktywny)[1]
            wartosci[ruch] = dziecko.wartosc
        ruch, wartosc = fun_por(wartosci.items(), key = klucz)
        wierzcholek.wartosc = wartosc
    return (ruch, wartosc)
