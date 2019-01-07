"""moduł realizuje algorytm alfa-beta odcinania"""
import parametry
import siatka
import wartosciowanie

LIMIT_POZIOMOW = 4
OCENA_REMISU = 0
_Gracze = {parametry.Faza.ALFA: None, parametry.Faza.BETA: None}

def inicjuj_graczy(gracz_alfa, gracz_beta):
    _Gracze[parametry.Faza.ALFA] = gracz_alfa
    _Gracze[parametry.Faza.BETA] = gracz_beta

def alfa_beta(stan_gry, biezaca_faza, poziom, limity):
    """stan_gry_zast: zastany stan gry wraz z ruchem który do niego doprowadził
    ostatni_ruch który doprowadził do zastana sytuacja
    biezaca_faza
    poziom - poziom drzewa
    limity - ograniczenia alfa i beta
    zwracane Ocena"""
    limity = limity.copy()
    # zastana sytuacja jest końcowa
    wstepna_ocena = wartosciowanie.max_strony(stan_gry, biezaca_faza)
    if abs(wstepna_ocena) >= siatka.WYGRYWAJACYCH:
        wyjscie = parametry.Ocena(stan_gry.ostatni_ruch, wstepna_ocena)
    elif stan_gry.siatka.jest_zapelniona():
        wyjscie = parametry.Ocena(stan_gry.ostatni_ruch, OCENA_REMISU)
    else:
        nastepne_ruchy = siatka.otoczenie(stan_gry.siatka)
        kont_petle = True
        while nastepne_ruchy and kont_petle:
            nast_ruch = nastepne_ruchy.pop()
            nast_siatka = stan_gry.siatka.copy()
            nast_siatka[nast_ruch] = _Gracze[biezaca_faza].symbol
            nast_stan = parametry.StanGry(siatka=nast_siatka,
                                          ostatni_ruch=nast_ruch)
            nast_ocena = alfa_beta(nast_stan,
                                   parametry.przeciwna(biezaca_faza),
                                   poziom + 1, limity)
            limity.warunkowo_aktualizuj(biezaca_faza, nast_ocena,
                                        nast_stan.ostatni_ruch)
            if limity.czy_ciecie():
                wyjscie = limity.pobierz(parametry.przeciwna(biezaca_faza))
                kont_petle = False
        if kont_petle:
            wyjscie = limity.pobierz(biezaca_faza)
    return wyjscie
