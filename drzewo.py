""" implementacja drzewa"""

class Wezel:
    def __init__(self, stan_siatki, ostatni_ruch, gracz):
        """buduje węzeł ze stan_siatki, ostatni_ruch przeciwnika i
        gracz który jest analizowany"""
        self.stan_siatki = stan_siatki
        self.ostatni_ruch = ostatni_ruch
        self.gracz = gracz
        self.wartosc = None
        self.dzieci = {} 

    def __setitem__(self, etykieta, podwezel):
        """do bierzącego węzła dodaj węzeł pod_wezel, etykietując go ruchem
        typu Polozenie"""
        self.dzieci[etykieta] = podwezel

    def keys(self):
        """podaje listę etykiet którymi oznaczone są poddrzewa"""
        return self.dzieci.keys()

    def __getitem__(self, etykieta):
        """zwraca poddrzewo etykietowane etykietą polozenie"""
        return self.dzieci.__getitem__(etykieta)
