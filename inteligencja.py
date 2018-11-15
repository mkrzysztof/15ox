import drzewo


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

def wartosciuj_wierzcholek(wierzcholek, ostatni_ruch):
    """ wartościuje wierzcholek w przypadku powodzenia ustawia zbiór wolnych
    pól siatki na puste, w pp wierzcholkowi nadawana jest wartość None"""
    siatka = wierzcholek.siatka
    aktywny_gracz = wierzcholek.gracz
    if siatka.jest_zapelniona():
        wierzcholek.wartosc = 0
        return
    if siatka.ma_uklad_wygrywajacy(ostatni_ruch):
        wierzcholek.wartosc = aktywny_gracz.mnoznik
        siatka.kasuj_wolne_pola()
    else:
        wierzcholek.wartosc = None

def dodaj_podwierzcholki(wierzcholek, stos):
    """ na podstawie zbioru wolnych pól na siatce dodaje
    do wierzcholka potomków reprezentujących następny ruch
    następnie umieść je na stosie"""
    wolne_pola = wierzcholek.siatka.wolne_pola()
    for ruch in wolne_pola:
        pod_wierzcholek = dodaj_ruch_na_siatce(wierzcholek, ruch)
        element = (pod_wierzcholek, ruch)
        stos.append(element)

def buduj_drzewo(stan_siatki, gracz_aktywny):
    przeciwnik = gracz_aktywny.przeciwnik
    wierzch_wyj = drzewo.Wierzcholek(stan_siatki, przeciwnik)
    stos = []
    element = (wierzch_wyj, None)
    stos.append(element)
    while stos:
        wierzcholek, ruch = stos.pop()
        wartosciuj_wierzcholek(wierzcholek, ruch)
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
            dziecko.wartosc = min_max(dziecko, gracz_aktywny)[1]
            wartosci[ruch] = dziecko.wartosc
        ruch, wartosc = fun_por(wartosci.items(), key=klucz)
        wierzcholek.wartosc = wartosc
    return (ruch, wartosc)
