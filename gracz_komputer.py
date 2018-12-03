""" moduł gracza komputerowego """
import time
import gracz
import inteligencja
import siatka
from monitoring import pokaz_wywolanie
import wartosciowanie

GLEBOKOSC = 6
FUN_WOLNE = siatka.wolne_pola
FUN_WART = wartosciowanie.klasyczne_plus_minus

FUN_OCENY = {"wolne": FUN_WOLNE, "wartosc": FUN_WART}

class GraczKomputer(gracz.Gracz):
    """Klasa reprezentująca komputer"""
    def __init__(self, symbol, nazwa="GRACZ-KOMPUTER"):
        super().__init__(symbol, nazwa="GRACZ-KOMPUTER")
    @pokaz_wywolanie
    def wyszukaj_wolne_pole(self, siatka_przesz):
        siatka_kopia = siatka_przesz.copy()
        self.mnoznik = 1
        self.przeciwnik.mnoznik = - 1
        czas = time.time()
        drzewo_decyzji = inteligencja.buduj_drzewo_stopnia(siatka_kopia, self,
                                                           GLEBOKOSC,
                                                           FUN_OCENY)
        print("zbudowano drzewo w {} sekund".format(time.time() - czas))
        czas = time.time()
        ruch, _ = inteligencja.min_max(drzewo_decyzji, self)
        print("obliczono min_max w {} sekund".format(time.time() - czas))
        return ruch
