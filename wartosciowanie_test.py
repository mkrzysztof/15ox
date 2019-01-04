import unittest
import unittest.mock
import parametry
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
        siatka1 = stworz_siatke(3, 3, wypelnienie)
        stan_gry = {
            "siatka": siatka1,
            "ostatni_ruch": siatka.Polozenie([0, 0])
            }
        testowany = wartosciowanie.klasyczne_plus_minus(stan_gry,
                                                        parametry.Faza.ALFA)
        self.assertEqual(1, testowany)

    def siatka2(self):
        pass

    def siatka3(self):
        pass

class TestMaxStrony(unittest.TestCase):
    wypelnienie1 = [
        [(0, 5), "x"],
        [(1, 2), "x"], [(1, 4), "x"],
        [(2, 2), "x"], [(2, 3), "x"], [(2, 4), "o"],
        [(3, 1), "x"], [(3, 2), "x"], [(3, 3), "x"], [(3, 4), "x"],
        [(3, 5), "x"],
        [(4, 1), "x"], [(4, 2), "x"],
        [(5, 0), "x"],
    ]

    def test1(self):
        siatka1 = stworz_siatke(10, 10, self.wypelnienie1)
        stan_gry = {"siatka": siatka1,
                    "ostatni_ruch": siatka.Polozenie((3, 2))}
        testowany = wartosciowanie.max_strony(stan_gry, parametry.Faza.ALFA)
        self.assertEqual(6, testowany)

    def test_3x3(self):
        wypelnienie = [
            [(0, 0), "o"], [(1, 0), "o"], [(2, 0), "o"],
            [(0, 1), "x"], [(0, 2), "x"],
        ]
        siatka_test = stworz_siatke(3, 3, wypelnienie)
        stan_gry = {"siatka": siatka_test,
                    "ostatni_ruch": siatka.Polozenie((2, 0))}
        testowany = wartosciowanie.max_strony(stan_gry, parametry.Faza.ALFA)
        self.assertEqual(3, testowany)


if __name__ == "__main__":
    unittest.main()
