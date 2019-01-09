"""moduł realizuje algorytm alfa-beta odcinania"""
import parametry
import siatka
import wartosciowanie


LIMIT_POZIOMOW = 10
OCENA_REMISU = 0
_Gracze = {parametry.Faza.ALFA: None, parametry.Faza.BETA: None}

def inicjuj_graczy(gracz_alfa, gracz_beta):
    """inicjujowanie przed użyciem modułu"""
    _Gracze[parametry.Faza.ALFA] = gracz_alfa
    _Gracze[parametry.Faza.BETA] = gracz_beta


def stworz_nowy_stan(stan_wej, faza, ruch):
    """zwraca nową siatkę powstałą po dodaniu ruchu przy danej fazie"""
    nast_siatka = stan_wej.siatka.copy()
    nast_siatka[ruch] = _Gracze[faza].symbol
    nast_stan = parametry.StanGry(siatka=nast_siatka, ostatni_ruch=ruch)
    return nast_stan

def alfa_beta(stan_gry, biezaca_faza, poziom, limity):
    """zwraca ocenę stanu gry
    stan_gry: zastany stan gry wraz z ruchem który do niego doprowadził
    ostatni_ruch który doprowadził do zastana sytuacja
    biezaca_faza
    poziom - poziom drzewa
    limity - ograniczenia alfa i beta"""
    limity = limity.copy()
    # zastana sytuacja jest końcowa
    wstepna_ocena = wartosciowanie.max_strony(stan_gry, biezaca_faza)
    if abs(wstepna_ocena) >= siatka.WYGRYWAJACYCH:
        wyjscie = parametry.Ocena(stan_gry.ostatni_ruch, wstepna_ocena)
    elif stan_gry.siatka.jest_zapelniona():
        wyjscie = parametry.Ocena(stan_gry.ostatni_ruch, OCENA_REMISU)
    elif poziom > LIMIT_POZIOMOW:
        wyjscie = parametry.Ocena(stan_gry.ostatni_ruch, wstepna_ocena)
    else:
        nastepne_ruchy = siatka.otoczenie(stan_gry.siatka)
        kont_petle = True
        while nastepne_ruchy and kont_petle:
            nast_ruch = nastepne_ruchy.pop()
            nast_stan = stworz_nowy_stan(stan_gry, biezaca_faza, nast_ruch)
            przeciwna_faza = parametry.przeciwna(biezaca_faza)
            nast_ocena = alfa_beta(nast_stan, przeciwna_faza, poziom + 1,
                                   limity)
            limity.warunkowo_aktualizuj(biezaca_faza, nast_ocena, nast_stan)
            if limity.czy_ciecie():
                wyjscie = limity.pobierz(przeciwna_faza)
                kont_petle = False
        if kont_petle:
            wyjscie = limity.pobierz(biezaca_faza)
    return wyjscie
