""" moduł gracza komputerowego """
import gracz
import inteligencja
import copy
from monitoring import pokaz_wywolanie

class GraczKomputer(gracz.Gracz):
    """Klasa reprezentująca komputer"""
    def __init__(self, symbol, nazwa="GRACZ"):
                super().__init__(symbol, nazwa="GRACZ")
    @pokaz_wywolanie
    def wyszukaj_wolne_pole(self, siatka):
        siatka_kopia = copy.deepcopy(siatka)
        self.mnoznik = 1
        self.przeciwnik.mnoznik = - 1
        drzewo_decyzji = inteligencja.buduj_drzewo(siatka_kopia, self)
        ruch, wartosc = inteligencja.min_max(drzewo_decyzji, self)
        return ruch
