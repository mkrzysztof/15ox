""" moduł gracza komputerowego """
import alfa_beta
import gracz
import siatka
import parametry
import symbole

GLEBOKOSC = 10
FUN_WOLNE = siatka.wolne_pola

# tu przechowuję informację o graczach komputerowym i człowieku
Gracze_Parametry = {
    "KOMPUTER": {"mnoznik": 1, "symbol": None},
    "CZLOWIEK": {"mnoznik": -1, "symbol": None}
    }

class GraczKomputer(gracz.Gracz):
    """Klasa reprezentująca komputer"""
    def __init__(self, symbol, nazwa="GRACZ-KOMPUTER"):
        super().__init__(symbol, nazwa="GRACZ-KOMPUTER")
        Gracze_Parametry["KOMPUTER"]["symbol"] = symbol
        Gracze_Parametry["CZLOWIEK"]["symbol"] = symbole.przeciwny(symbol)

    def wyszukaj_wolne_pole(self, ostatnie_polozenie, siatka_przesz):
        oceny = parametry.nowe_ograniczenia()
        stan_poczatkowy = parametry.StanGry(siatka=siatka_przesz,
                                            ostatni_ruch=ostatnie_polozenie)
        ocena_ruchu = alfa_beta.alfa_beta(stan_poczatkowy, parametry.Faza.ALFA,
                                          0, oceny)
        print("oceniony ruch = ", ocena_ruchu)
        return ocena_ruchu.pokaz_ruch()
