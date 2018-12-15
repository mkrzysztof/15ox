"""moduł realizuje algoirytm alfa-beta odcinania"""

import enum
import gracz_komputer
import siatka

def _przeciwna(faza):
    #odwraca fazę na przeciwną
    return "beta" if faza == "alfa" else "alfa"

_PUSTE = siatka.Polozenie() # pusty ruch

_LIMIT_POZIOM = 2
def _brak_konca(glebokosc, ocena):
    # prawda jeśli głebokość nie przekroczyła dopuszczalny limit
    # lub sytuacja nie jest wygrana
    return glebokosc < _LIMIT_POZIOM and abs(ocena) < siatka.WYGRYWAJACYCH

def _przeciwnik(gracz):
    return "CZLOWIEK" if gracz == "KOMPUTER" else "KOMPUTER"

def _dodaj_ruch(gracz, stan_gry, ruch):
    # zwraca stan_gry po dodaniu ruchu
    # gracz - to "CZLOWIEK", "KOMPUTER"
    nowa_siatka = stan_gry["siatka"].copy()
    nowa_siatka[ruch] = gracz_komputer.Gracze[gracz]["symbol"]
    return {"siatka": nowa_siatka, "ostatni_ruch": ruch}

def alfa_beta(stan_gry, glebokosc, ograniczenie, fun_oceny, fun_wolne, faza):
    """wykonuje algorytm alfa-beta, z danego stan_gry, znajdując się 
    na biez_poziom "myślenia", będąc w wybranej fazie, mając daną funcję oceny
    i funkcję wyznaczającą ruchy do wykonania. 
    Zwraca parę (wartość_ruchu, wybrany_ruch)

    stan_gry - stan przed wykonaniem ruchu
    glebokosc - głębokość na której przeszukiwane jest drzewo gry
    ograniczenie - słownik {"alfa": int, "beta": int}
    fun_oceny - funkcja oceniająca na podstawie stanu gry sytuację
    faza - <"alfa", "beta"> - jedna z faz w której znajduje się
    algorytm"""
    def _ocen_ruch(nowy_ruch, ograniczenia):
        nowy_stan = _dodaj_ruch(gracz_oceniany, stan_gry, ruch)
        ocena_nowy, _ = alfa_beta(nowy_stan, glebokosc+1, ograniczenie,
                                  fun_oceny,
                                  fun_wolne, _przeciwna(faza))
        return ocena_nowy
    porownanie = {"alfa": max, "beta": min} # funkcje porównujące
    fazy_graczy = {"alfa": "KOMPUTER", "beta": "CZLOWIEK"}
    gracz_oceniany = fazy_graczy[faza]
    ruch_wyj = stan_gry["ostatni_ruch"]
    ocena = fun_oceny(stan_gry, _przeciwnik(gracz_oceniany)) # oceniamy korzeń
    if _brak_konca(glebokosc, ocena):
        ocena = 0
        ruchy_iter = iter(fun_wolne(stan_gry["siatka"]))
        ruch_wyj = ruch = next(ruchy_iter, _PUSTE)
        while ruch:
            ocena_nowy = _ocen_ruch(ruch, ograniczenia)
            print("max czy min", porownanie[faza], faza)
            ograniczenie[faza] = porownanie[faza](ograniczenie[faza],
                                                  ocena_nowy)
            ocena = ograniczenie[faza]
            if ograniczenie["alfa"] >= ograniczenie["beta"]:
                ocena = ograniczenie[_przeciwna(faza)]
                ruch = _PUSTE
            ruch_wyj = ruch
            ruch = next(ruchy_iter, _PUSTE)
    return (ocena, ruch_wyj)
