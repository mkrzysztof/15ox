"""odpowiada za inteligencję, głównie budowa i ocena drzewa gry"""
import drzewo
import siatka
import wartosciowanie

LIMIT = 3

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

def _ocen_lub_dodaj(wierzcholek, licznik_stopnia, fun_oceny, ostatni_ruch,
                    stos):
    """w zależności od sytuacji oceń wierzchołek, lub dodaj do niego
    podwierzchołki, wkładając je na stos, wolne wierzchołki określa funkcja
    fun_wolne, dla ostatnio wykonanego ruchu"""
    siatka_wierzch = wierzcholek.siatka
    ocena = _wartosciuj_wierzcholek(wierzcholek, ostatni_ruch,
                                    fun_oceny["wartosc"])
    if siatka_wierzch.jest_zapelniona():
        wierzcholek.wartosc = 0
    elif siatka_wierzch.ma_uklad_wygrywajacy(ostatni_ruch):
        wierzcholek.wartosc = ocena
    else:
        _dodaj_podwierzcholki(wierzcholek, stos, licznik_stopnia + 1,
                              fun_oceny["wolne"])

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

def buduj_drzewo_stopnia(stan_siatki, gracz_aktywny, glebokosc, fun_oceny):
    """buduj drzewo o zadanej głębokości. Korzeń zawiera sytuację po ostatnim
    ruchu przeciwnika.W przypadku początku gry jest pusta siatka """
    stos = []
    wierzch_wyj = _stworz_korzen(stan_siatki, gracz_aktywny, stos)
    while stos:
        wierzcholek, ruch, licznik_stopnia = stos.pop()
        if licznik_stopnia < glebokosc:
            _ocen_lub_dodaj(wierzcholek, licznik_stopnia, fun_oceny, ruch,
                            stos)
        else:
            ocena = _wartosciuj_wierzcholek(wierzcholek, ruch,
                                            fun_oceny["wartosc"])
            wierzcholek.wartosc = ocena
        wierzcholek.siatka = None
    return wierzch_wyj

def _klucz(lst):
    return lst[1]

def dodaj_ruch(siatka, ruch, gracz):
    """ dodaje ruch do siatki
    gracz - gracz który wykonuje ruch
    zwraca parę siatka + ruch, ruch"""
    nast_siatka = siatka.copy()
    nast_siatka[ruch] = gracz.symbol
    return (nast_siatka, ruch)

def stan_jest_koncowy(stan):
    siatka, ostatni_ruch = stan
    return (siatka.jest_zapelniona()
            or siatka.ma_uklad_wygrywajacy(ostatni_ruch))

def alfa_max(stan, gracz, poziom, fun_oceny):
    """faza alfa algorytmu alfa-beta,
    stan - stan gry (siatka, ostatni ruch)\
    fun_oceny - funkcja wartości i funkcja otoczenia dla siatki
    gracz - gracz dla którego puszczony jest algorytm alfa-beta"""
    global alfa, beta
    fun_wart = fun_oceny["wartosc"]
    fun_wolne = fun_oceny["wolne"]
    siatka, ostatni_ruch = stan
    ruch_wyj = ostatni_ruch
    ocena = fun_wart(siatka, gracz.przeciwnik, ostatni_ruch)
    if (poziom < LIMIT and not siatka.ma_uklad_wygrywajacy(ostatni_ruch)):
        mozliwe_ruchy = fun_wolne(siatka)
        print("mozliwe ruchy: ", mozliwe_ruchy)
        for ruch in mozliwe_ruchy:
            ruch_wyj = ruch
            stan_prim = dodaj_ruch(siatka, ruch, gracz)
            bmin, _ = beta_min(stan_prim, gracz, poziom + 1,
                               fun_oceny)
            alfa = max(alfa, bmin)
            if alfa >= beta:
                ocena = beta
                break
        ocena = alfa
    assert ocena is not None
    print("ruch alfa = ", ruch_wyj, ocena)
    return (ocena, ruch_wyj)

def beta_min(stan, gracz, poziom, fun_oceny):
    """analogicznie do alfa_max, gracz - to gracz dla którego puszczony
    jest algorytm poszukiwania ruchu"""
    global alfa, beta
    fun_wart = fun_oceny["wartosc"]
    fun_wolne = fun_oceny["wolne"]
    siatka, ostatni_ruch = stan
    ruch_wyj = ostatni_ruch
    ocena = fun_wart(siatka, gracz, ostatni_ruch)
    if (poziom < LIMIT and not siatka.ma_uklad_wygrywajacy(ostatni_ruch)):
        mozliwe_ruchy = fun_wolne(siatka)
        print("mozliwe ruchy: ", mozliwe_ruchy)
        for ruch in mozliwe_ruchy:
            ruch_wyj = ruch
            stan_prim = dodaj_ruch(siatka, ruch, gracz)
            amax, _ = alfa_max(stan_prim, gracz, poziom + 1,
                               fun_oceny)
            beta = min(beta, amax)
            if beta >= alfa:
                ocena = alfa
                break
        ocena = beta
    assert ocena is not None
    print("ruch beta = ", ruch_wyj, ocena)
    return (ocena, ruch_wyj)

def min_max(stan, gracz):
    global alfa, beta
    alfa = -100000
    beta =  100000
    poziom = 0
    fun_oceny = {"wolne": siatka.wolne_pola,
                 "wartosc": wartosciowanie.max_strony}
    _, ruch = alfa_max(stan, gracz, poziom, fun_oceny)
    print("------")
    return ruch, None
