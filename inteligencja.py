import drzewo
import siatka
import gracz
import sys


def buduj_drzewo(stan_siatki, ostatni_ruch, gracz_aktywny):
    przeciwnik = gracz_aktywny.przeciwnik
    wierz_wyj = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    if stan_siatki.jest_zapelniona:
        wierz_wyj.wartosc = 0
    elif stan_siatki.ma_uklad_wygrywajacy(ostatni_ruch):
        wierz_wyj.wartosc = przeciwnik.mnoznik
    else:
        for ruch in stan_siatki.wolne_pola():
            nastepna_siatka = copy.copy(stan_siatki)
            nastepna_siatka.zapis_polozenie(ruch, gracz_aktywny.symbol)
            poddrzewo = buduj_drzewo(nastepna_siatka, ruch, przeciwnik)
            wierz_wyj[ruch] = poddrzewo
    return wierz_wyj
