import zarzadca


class Symbol(object):
    """klasa abstrakcyjna reprezentująca kółko lub krzyżykl"""
    repr_graf = None
    repr = None
    komunikat = None

    @classmethod
    def postaw_na_planszy(cls, plansza, polozenie):
        """postaw na planszy symbol na pozycji"""
        pozycja = tuple(polozenie)
        plansza[polozenie] = cls
        zarzadca.rozeslij(cls.komunikat, cls, pozycja, plansza.surface)

class Kolko(Symbol):
    """sybol kółka"""
    #repr_graf = grafika.Kolko_graf()
    repr = "o"
    komunikat = "kolko"

class Krzyzyk(Symbol):
    """symbol krzyżyk"""
    #repr_graf = grafika.Krzyzyk_graf()
    repr = "x"
    komunikat = "krzyzyk"

class Puste(Symbol):
    """pusty"""
    repr = "."
