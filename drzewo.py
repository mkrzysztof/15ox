class Wierzcholek:
    __slots__ = ["siatka", "gracz", "wartosc", "__dzieci"]
    def __init__(self, stan_siatki, gracz):
        self.siatka = stan_siatki
        self.gracz = gracz
        self.wartosc = None
        self.__dzieci = {}

    def __setitem__(self, klucz, wierzcholek):
        self.__dzieci[klucz] = wierzcholek

    def __getitem__(self, klucz):
        return self.__dzieci[klucz]

    def keys(self):
        return self.__dzieci.keys()
