import grafika
import plansza
import zarzadca

class Symbol(object):
    """klasa abstrakcyjna reprezentująca kółko lub krzyżykl"""
    repr_graf = None
    repr = None

    @classmethod
    def postaw_na_planszy(cls, plansza, polozenie):
        """postaw na planszy symbol na pozycji"""
        pozycja = tuple(polozenie)
        plansza.zapis_polozenie(polozenie, cls)
        zarzadca.rozeslij(pozycja, plansza.surface, cls.repr_graf)

class Kolko(Symbol):
    """sybol kółka"""
    repr_graf = grafika.Kolko_graf()
    repr = "o"

class Krzyzyk(Symbol):
    """symbol krzyżyk"""
    repr_graf = grafika.Krzyzyk_graf()
    repr = "x"

class Puste(Symbol):
    """pusty"""
    repr = "."
