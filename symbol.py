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
        zarzadca.rozeslij(cls.repr_graf, pozycja, plansza.surface)

class Kolko(Symbol):
    """sybol kółka"""
    repr_graf = grafika.Kolko_graf()
    repr = "Kolko"

class Krzyzyk(Symbol):
    """symbol krzyżyk"""
    repr_graf = grafika.Krzyzyk_graf()
    repr = "Krzyzyk"
