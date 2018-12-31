"""moduł realizuje algoirytm alfa-beta odcinania"""
import copy
import operator
import gracz_komputer
import siatka
import wartosciowanie

GRACZE = {"ALFA" : "KOMPUTER",
          "BETA": "CZLOWIEK"}
LIMIT = 4


class OcenaRuchu:
    """struktura ma przedstawiać wartość czyli ocena, oraz argument czyli
    ruch który realizuje tą wartość"""
    def __init__(self):
        self.ocena = None
        self.ruch = None

    def __repr__(self):
        return "ocena = {0}, ruch = {1}".format(self.ocena, self.ruch)

    def __eq__(self, value):
        return (self.ocena == value.ocena
                and self.ruch == value.ruch)

    def __gt__(self, value):
        return self.ocena.__gt__(value.ocena)

    def __ge__(self, value):
        return self.ocena.__ge__(value.ocena)

    def __lt__(self, value):
        return self.ocena.__lt__(value.ocena)

    def __le__(self, value):
        return self.ocena.__le__(value.ocena)

def przeciwny(etap):
    return "BETA" if etap == "ALFA" else "ALFA"

def czy_to_koniec(siatka_wej, ruch, etap, poziom):
    stan_gry = {"siatka": siatka_wej, "ostatni_ruch": ruch}
    koniec = False
    ocena = wartosciowanie.max_strony(stan_gry, GRACZE[etap])
    if poziom < LIMIT:
        if abs(ocena) >= siatka.WYGRYWAJACYCH:
            koniec = True
        elif siatka_wej.jest_zapelniona():
            koniec = True
    else:
        koniec = True
    return koniec

def ocen_sytuacje(siatka_wej, ostatni_ruch, gracz):
    stan_gry = {"siatka": siatka_wej, "ostatni_ruch": ostatni_ruch}
    wyjscie = OcenaRuchu()
    ocena = wartosciowanie.max_strony(stan_gry, gracz)
    wyjscie.ruch = ostatni_ruch
    wyjscie.ocena = ocena
    return wyjscie

def stworz_siatke(siatka_wej, ruch, symbol):
    siatka_wyj = siatka_wej.copy()
    siatka_wyj[ruch] = symbol
    return siatka_wyj

_porownanie = {"ALFA": operator.gt, "BETA":operator.lt}
def alfa_beta(siatka_wej, ruch, oceny, poziom, etap):
    """zwraca ocenę i ruch które są w danej chwili najlepsze
    na podstawie ostatnio wykonanego ruchu, mając dane oceny,
    przy danym poziomie na danym etapie
    siatka - typu Siatka
    ruch - typu Polozenie
    oceny - słownik z kluczami "ALFA", "BETA" o wartościach OcenaRuchu
    etap {"ALFA", "BETA"} """
    przeciwny_etap = przeciwny(etap)
    biezacy_parametry = gracz_komputer.Gracze_Parametry[GRACZE[etap]]
    if czy_to_koniec(siatka_wej, ruch, etap, poziom):
        wyjscie = ocen_sytuacje(siatka_wej, ruch, GRACZE[przeciwny_etap])
    else:
        oceny = copy.copy(oceny)
        dostepne_ruchy = siatka.otoczenie(siatka_wej)
        for wolny_ruch in dostepne_ruchy:
            ostatni_ruch = wolny_ruch
            nast_siatka = stworz_siatke(siatka_wej, wolny_ruch,
                                        biezacy_parametry["symbol"])
            wynik = alfa_beta(nast_siatka, wolny_ruch, oceny,
                              poziom + 1, przeciwny_etap)
            if etap == "ALFA":
                ocena_alfa = oceny["ALFA"].ocena
                oceny[etap].ocena = max(oceny[etap].ocena, wynik.ocena)
                if oceny[etap].ocena != ocena_alfa:
                    oceny[etap].ruch = wolny_ruch
                if oceny["ALFA"] >= oceny["BETA"]:
                    wyjscie = oceny["BETA"]
                    wyjscie.ruch = oceny["ALFA"].ruch
                    break
            if etap == "BETA":
                ocena_beta = oceny["BETA"].ocena
                oceny[etap].ocena = min(oceny["BETA"].ocena, wynik.ocena)
                if oceny[etap].ocena != ocena_beta:
                    oceny[etap].ruch = wolny_ruch
                if oceny["ALFA"] >= oceny["BETA"]:
                    wyjscie = oceny["ALFA"]
                    wyjscie.ruch = oceny["BETA"].ruch
                    break
        wyjscie = oceny[etap]
        wyjscie.ruch = ostatni_ruch
    return wyjscie
