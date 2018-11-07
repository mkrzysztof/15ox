import drzewo
import siatka
import gracz
import time


def _nastepny_wierzcholek(wierzcholek, ruch):
    """ stwórz wierzchołek odpowiadający ruchowi przeciwnika """
    przeciwnik = wierzcholek.gracz.przeciwnik
    kopia_siatki = wierzcholek.siatka.copy()
    kopia_siatki[ruch] = przeciwnik.symbol
    return drzewo.Wierzcholek(kopia_siatki, przeciwnik)

def _ocen_wierzcholek(wierzcholek, ostatni_ruch):
    """ na podstawie siatki w wierzchołku i ostatniego ruchu oceń
    wierzchołek None oznacza brak oceny """
    ocena = None
    gracz = wierzcholek.gracz
    siatka = wierzcholek.siatka
    if ostatni_ruch is not None:
        if siatka.ma_uklad_wygrywajacy(ostatni_ruch):
            ocena = gracz.mnoznik
        elif siatka.jest_zapelniona():
            ocena = 0
    return ocena

def _dolacz_poddrzewa(korzen):
    wolne_ruchy = korzen.siatka.wolne_pola()
    for ruch in wolne_ruchy:
        potomek = _nastepny_wierzcholek(korzen, ruch)
        korzen[ruch] = potomek
        stworz_drzewo(potomek, ruch)

stat_licznik = 0
def stworz_drzewo(korzen, ostatni_ruch):
    global stat_licznik
    stat_licznik += 1
    ocena = _ocen_wierzcholek(korzen, ostatni_ruch)
    if ocena is None:
        _dolacz_poddrzewa(korzen)
    else:
        korzen.wartosc = ocena

def buduj_drzewo(stan_siatki, gracz_aktywny):
    # ruch aktywnego gracza poprzedza stan jego przeciwnika pusta plansza
    przeciwnik = gracz_aktywny.przeciwnik
    korzen = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    stworz_drzewo(korzen, None)
    print("stat licznik = {}".format(stat_licznik))
    return korzen

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
            dziecko = wierzcholek[ruch]
            dziecko.wartosc = min_max(dziecko, gracz_aktywny)[1]
            wartosci[ruch] = dziecko.wartosc
            ruch, wartosc = fun_por(wartosci.items(), key = klucz)
        wierzcholek.wartosc = wartosc
    return (ruch, wartosc)
