import siatka

class Plansza:
    """reprezentuje planszę na której rozgrywana jest gra:
    siatka gry + informacje"""

    def __init__(self, surface, wierszy=15, kolumn=15):
        """ surface obiekt pygame.surface """
        self.pola = siatka.Siatka(wierszy, kolumn)
        self.wierszy = wierszy
        self.kolumn = kolumn
        self.surface = surface

    def zapis_polozenie(self, polozenie, symbol):
        """postawienie symbol na Plansza na polozenie"""
        self.pola.zapis_polozenie(polozenie, symbol)

    def jest_zapelniona(self):
        return self.pola.jest_zapelniona()

    def ma_uklad_wygrywajacy(self, polozenie):
        """szukaj układu wygrywającego wok1ół pozycji pozycja,
        w 4 kierunkach
        """
        return self.pola.ma_uklad_wygrywajacy(polozenie)
