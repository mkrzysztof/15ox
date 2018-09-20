import grafika

class Gracz(object):
    """Klasa abstrakcyjna reprezentująca dowoilnego gracza"""
    def __init__(self, symbol, nazwa="GRACZ"):
        self.symbol = symbol
        self.wygrana = False
        self.mnoznik = 0
        self.przeciwnik = None
        self.nazwa = nazwa

    def wyszukaj_wolne_pole(self, siatka):
        """metoda obstrakcyjna zwraca siatka.Polozenie reprezentującą położenie
        na polu planszy """
        pass

    def postaw_symbol_na_planszy(self, plansza):
        polozenie = self.wyszukaj_wolne_pole(plansza.pola)
        self.symbol.postaw_na_planszy(plansza, polozenie)
        return polozenie

    def ustaw_wygrana(self):
        self.wygrana = True
        print("wygrana")


class GraczCzlowiek(Gracz):
    """Klasa reprezentująca człowieka"""

    def wyszukaj_wolne_pole(self, siatka):
        zla_pozycja = True
        while zla_pozycja:
            polozenie = grafika.odczyt_poz_myszy()
            if (polozenie.nie_wychodzi_poza(siatka)
                    and polozenie.jest_puste(siatka)):
                zla_pozycja = False
        return polozenie

class GraczKomputer(Gracz):
    """Klasa reprezentująca komputer"""
    pass
