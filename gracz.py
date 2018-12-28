"""implementacja gracza"""
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

    def dodaj_przeciwnika(self, przeciwnik):
        """ustala przeciwnika"""
        self.przeciwnik = przeciwnik
        przeciwnik.przeciwnik = self

    def postaw_symbol_na_planszy(self, ostatnie_polozenie, plansza):
        """wybiera dogodne położenie i stawia na niej swój symbol
        zwraca to położenie"""
        polozenie = self.wyszukaj_wolne_pole(ostatnie_polozenie, plansza.pola)
        self.symbol.postaw_na_planszy(plansza, polozenie)
        return polozenie

    def ustaw_wygrana(self):
        """ustawia, że gracz wygrał"""
        self.wygrana = True
        print("wygrana")


class GraczCzlowiek(Gracz):
    """Klasa reprezentująca człowieka"""

    def wyszukaj_wolne_pole(self, ostatnie_polozenie, siatka):
        zla_pozycja = True
        while zla_pozycja:
            polozenie = grafika.odczyt_poz_myszy()
            if (siatka.zawiera_polozenie(polozenie)
                    and siatka[polozenie] is None):
                zla_pozycja = False
        return polozenie
