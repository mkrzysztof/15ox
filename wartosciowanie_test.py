import unittest
import unittest.mock
import siatka
import wartosciowanie


def stworz_siatke(wierszy, kolumn, wypelnienie):
    """ wypelnienie jest postaci:
    [
    [(w, k), symbol],
    [(w, k), symbol],
    .
                .
    ] 
    pustych nie umieszczamy"""
    a_siatka = siatka.Siatka(wierszy, kolumn)
    for polozenie, symbol in wypelnienie:
        a_siatka[siatka.Polozenie(polozenie)] = symbol
    return a_siatka

class TestWartosciowanie(unittest.TestCase):

    
        
    
    def test_siatka1(self):
        """ siatka
        xxx
        o.o
        o.. """
        wypelnienie = [
            [(0, 0), "x"], [(0, 1), "x"], [(0, 2), "x"],
            [(1, 0), "o"], [(1, 2), "o"],
            [(2, 0), "o"],
        ]
        gracz = unittest.mock.Mock()
        gracz.mnoznik = 1
        siatka1 = stworz_siatke(3, 3, wypelnienie)
        testowany = wartosciowanie.klasyczne_plus_minus(
            siatka1, gracz, siatka.Polozenie((0, 1))
        )
        self.assertEqual(1, testowany)
        
    def siatka2(self):
        pass

    def siatka3(self):
        pass

    


if __name__ == "__main__":
    unittest.main()
