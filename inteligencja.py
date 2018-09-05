import siatka
import drzewo

def buduj_drzewo(stan_siatki, ostatni_ruch, gracz_aktywny):
    przeciwnik = aktywny_gracz.przeciwnik
    wierz_wyj = drzewo.Wierzcholek(stan_siatki, ostatni_ruch, przeciwnik)
    if stan_siatki.jest_zapelniona():
        wierz_wyj.wartosc = 0
    elif stan_siatki.ma_uklad_wygrywajacy(ostatni_ruch):
        wierz_wyj.wartosc = przeciwnik.mnoznik
    else:
        for ruch in stan_siatki.wolne_pola():
            nastepna_siatka = copy.copy(stan_siatki)
            nastepna_siatka.zapis_polozenia(ruch, aktywny_gracz.symbol)
            pod_drzewo = buduj2_drzewo(nastepna_siatka, ruch, przeciwnik)
            wierz_wyj[ruch] =  pod_drzewo
    
