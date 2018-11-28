"""implementacja wierzchołka drzewa"""
class Wierzcholek(dict):
    """stworzenie wierzchołka na podstawie sytuacji na planszy dla
    danego  gracza"""
    def __init__(self, stan_siatki, gracz):
        super().__init__()
        self.siatka = stan_siatki
        self.gracz = gracz
        self.wartosc = None
