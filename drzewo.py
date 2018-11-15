class Wierzcholek(dict):
    def __init__(self, stan_siatki, gracz):
        super().__init__()
        self.siatka = stan_siatki
        self.gracz = gracz
        self.wartosc = None
