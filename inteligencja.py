import drzewo
import siatka
import gracz

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
            nastepna_siatka = siatka.copy()
            nastepna_siatka.zapis_polozenie(ruch, gracz.przeciwnik.symbol)
            pod_wierzcholek = drzewo.Wierzcholek(nastepna_siatka,
                                                 gracz.przeciwnik)
            wierzcholek.dodaj(ruch, pod_wierzcholek)
            element = (pod_wierzcholek, ruch, glebokosc)
            stos.append(element)
        wierzcholek.siatka = None
    return wierzch_wyj

def min_max(wierzcholek, gracz_aktywny):
    wartosc = wierzcholek.wartosc
    ruch = None
    if wartosc is None:
        wartosci = {}
        for ruch in wierzcholek.keys():
            dziecko = wierzcholek.odczytaj(ruch)
            dziecko.wartosc = min_max(dziecko, gracz_aktywny)[1]
            wartosci[ruch] = dziecko.wartosc
        if wierzcholek.gracz != gracz_aktywny:
            ruch, wartosc = max(wartosci.items(), key = lambda x: x[1])
        else:
            ruch, wartosc = min(wartosci.items(), key = lambda x: x[1])
        wierzcholek.wartosc = wartosc
    return (ruch, wartosc)
