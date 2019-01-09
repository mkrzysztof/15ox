import unittest as ut
import siatka
import symbole

WIERSZY = 0
KOLUMN = 1

def zbuduj_siatke(polozenia, wymiar=(3, 3)):
    # polozenia mają format słownika
    # "KOLKO" :   lista krotek reprezentująca położenia
    # "KRZYZYK" : ----------------------"-------------
    # zwraca obiekt siatka
    budowana_siatka = siatka.Siatka(*wymiar)
    for symbol in [symbole.Kolko, symbole.Krzyzyk]:
        for poz in polozenia[symbol]:
            budowana_siatka[siatka.Polozenie(poz)] = symbol
    return budowana_siatka

class TestPolozenie(ut.TestCase):
    testowe = [
        [siatka.Polozenie((0, 0)), siatka.PRAWO, siatka.Polozenie((0, 1))],
        [siatka.Polozenie((0, 0)), siatka.DOL, siatka.Polozenie((1, 0))],
        [siatka.Polozenie((3, 4)), siatka.DOL, siatka.Polozenie((3+1, 4+0))],
        [siatka.Polozenie((3, 4)), siatka.PRAWO, siatka.Polozenie((3, 4+1))],
        [siatka.Polozenie((3, 4)), siatka.LEWO, siatka.Polozenie((3, 4-1))],
        [siatka.Polozenie((3, 4)), siatka.GORA, siatka.Polozenie((3-1, 4))],
        [siatka.Polozenie((3, 4)), siatka.PRAWO, siatka.Polozenie((3, 4+1))],
        [siatka.Polozenie((3, 4)), siatka.LEWO_GORA,
         siatka.Polozenie((3-1, 4-1))],
        [siatka.Polozenie((3, 4)), siatka.LEWO_DOL,
         siatka.Polozenie((3+1, 4-1))],
        [siatka.Polozenie((3, 4)), siatka.PRAWO_GORA,
         siatka.Polozenie((3-1, 4+1))],
        [siatka.Polozenie((3, 4)), siatka.PRAWO_DOL,
         siatka.Polozenie((3+1, 4+1))],
    ]
    def test_przesun(self):
        for polozenie, przes, wynik in self.testowe:
            testowany = polozenie.przesun(przes)
            self.assertEqual(wynik, testowany)

class TestSiatka(ut.TestCase):
    test1 = (((siatka.Siatka(3, 4), siatka.Polozenie((1, 2))), True),
             ((siatka.Siatka(3, 4), siatka.Polozenie((1, 5))), False),
             ((siatka.Siatka(3, 4), siatka.Polozenie((1, 4))), False)
    )
    def test_zawiera_polozenie(self):
        for arg, wynik in self.test1:
            s, p = arg
            testowany = s.zawiera_polozenie(p)
            self.assertEqual(wynik, testowany)

    # jest_zapelniona

    #jest zapełniona całkowicie
    
    w = 10
    k = 10
    pola_zap = None
    def zapelnij_pola_zap(w, k):
        TestSiatka.pola_zap = set(siatka.Polozenie((x, y))
                       for x in range(w)
                       for y in range(k))
    
    def testuj_jest_zapelniona_zap(self):
        siatka_zap = siatka.Siatka(self.w, self.k)
        self.__class__.zapelnij_pola_zap(self.w, self.k)
        for p in TestSiatka.pola_zap:
            siatka_zap[p] = "x"
        self.assertEqual(True, siatka_zap.jest_zapelniona())

    # nie jest całkowicie zapełniona
    def testuj_jest_zapelniona_nie(self):
        siatka_nie = siatka.Siatka(self.w, self.k)
        siatka_nie[siatka.Polozenie((1,1))] = "x"
        self.assertEqual(False, siatka_nie.jest_zapelniona())

    def test_policz_symbol(self):
        def polozenie(x, y):
            return siatka.Polozenie((x, y))
        symbol = "x"
        siatka_t = siatka.Siatka(10, 10)
        siatka_t[polozenie(2,2)] = symbol
        siatka_t[polozenie(2,3)] = symbol
        siatka_t[polozenie(2,4)] = symbol
        siatka_t[polozenie(2,6)] = symbol
        ile = siatka_t.policz_symbol(symbol, polozenie(2,2), siatka.PRAWO)
        self.assertEqual(3, ile)
        ile = siatka_t.policz_symbol(symbol, polozenie(2,2), siatka.LEWO)
        self.assertEqual(1, ile)
        ile = siatka_t.policz_symbol(symbol, polozenie(2,4), siatka.LEWO)
        self.assertEqual(3, ile)
        ile = siatka_t.policz_symbol(symbol, polozenie(1,2), siatka.LEWO)
        self.assertEqual(0, ile)

    siatki = [siatka.Siatka(10, 10), siatka.Siatka(10, 10),]
    polozenia = [siatka.Polozenie((2, 3)),
                 siatka.Polozenie((0, 0)),
    ]
    wyniki = [
        set(
            [siatka.Polozenie((1, 2)), siatka.Polozenie((1, 3)),
             siatka.Polozenie((1, 4)),
             siatka.Polozenie((2, 2)), siatka.Polozenie((2, 4)),
             siatka.Polozenie((3, 2)), siatka.Polozenie((3, 3)),
             siatka.Polozenie((3, 4)),]
        ),
        set(
            [siatka.Polozenie((0, 1)),
             siatka.Polozenie((1, 0)), siatka.Polozenie((1, 1)),]
        ),
    ]
    
    def test_otoczenie(self):
        for s, p, w in zip(self.siatki, self.polozenia, self.wyniki):
            s[p] = "x"
            testowany = s.otoczenie()
            self.assertEqual(w, testowany)

    def test_otoczenie2(self):
        test_siatka = zbuduj_siatke(
            {symbole.Kolko: [(2, 2), (1, 1)],
             symbole.Krzyzyk: [(1, 0), (1, 2)]}
             )
        otoczenie = {siatka.Polozenie(k) for k in [(0, 0), (0, 1), (0, 2),
                                                   (2, 0), (2, 1)]}
        otocz_siatka = test_siatka.otoczenie()
        self.assertEqual(otoczenie, otocz_siatka)


if __name__ == "__main__":
    ut.main()
