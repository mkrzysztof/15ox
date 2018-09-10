class Wierzcholek:
    def __init__(self, stan_siatki, gracz):
        nazwa = None
        self.siatka = stan_siatki
        self.gracz = gracz
        self.wartosc = None
        self.__dzieci = {}

    def __setattr__(self, klucz, wierzcholek):
        self.__dzieci[klucz] = wierzcholek

    def __getattr__(self, klucz):
        return self.__dzieci[klucz]

    def keys(self):
        return self.__dzieci.keys()
