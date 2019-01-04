import unittest
import parametry

class FazaTest(unittest.TestCase):
    def test_alfa(self):
        faza_alfa = parametry.Faza.ALFA
        wlasciwy_wynik = parametry.Faza.BETA
        wynik = parametry.przeciwna(faza_alfa)
        self.assertEqual(wlasciwy_wynik, wynik)

    def test_beta(self):
        faza_beta = parametry.Faza.BETA
        wlasciwy_wynik = parametry.Faza.ALFA
        wynik = parametry.przeciwna(faza_beta)
        self.assertEqual(wlasciwy_wynik, wynik)

    def test_mnoznik(self):
        dane = [parametry.Faza.ALFA, parametry.Faza.BETA]
        wlasciwe = [1, -1]
        wyniki = [parametry.mnoznik(d) for d in dane]
        for wlasciwy, wynik in zip(wlasciwe, wyniki):
            self.assertEqual(wlasciwy, wynik)

class OcenaTest(unittest.TestCase):
    def test_wymien(self):
        ocena = parametry.Ocena("r1", 10)
        ruch2 = "r2"
        wzorcowy = parametry.Ocena("r2", 10)
        ocena.wymien_ruch(ruch2)
        self.assertEqual(wzorcowy._ruch, ocena._ruch)

    def test_mniejsza(self):
        ocena1 = parametry.Ocena("r1", 8)
        ocena2 = parametry.Ocena("r2", 10)
        self.assertEqual(ocena1.mniejsza(ocena2), True)

    def test_wieksza(self):
        ocena1 = parametry.Ocena("w1", 23)
        ocena2 = parametry.Ocena("w3", 14)
        self.assertEqual(ocena1.wieksza(ocena2), True)

    def test_wieksza_rowna(self):
        oceny1 = [parametry.Ocena("a", 10), parametry.Ocena("b", 7)]
        oceny2 = [parametry.Ocena("f", 4), parametry.Ocena("g", 7)]
        for oc1, oc2 in zip(oceny1, oceny2):
            self.assertEqual(oc1.wieksza_rowna(oc2), True)

class GraczeTest(unittest.TestCase):    
    def test_gracze_faza(self):
        gracze = parametry.Gracze("GRACZ_A", "GRACZ_B")
        fazy = [parametry.Faza.ALFA, parametry.Faza.BETA]
        wlasciwe = ["GRACZ_A", "GRACZ_B"]
        wyniki = [gracze.gracz_w_fazie(f) for f in fazy]
        for wlasciwy, wynik in zip(wlasciwe, wyniki):
            self.assertEqual(wlasciwy, wynik)

class OgraniczeniaTest(unittest.TestCase):
    def test_aktualizuj(self):
        ogr = parametry.Ograniczenia()
        ocena = parametry.Ocena("x", 10)
        ogr.aktualizuj(parametry.Faza.ALFA, ocena, "y")
        self.assertEqual(ogr._ograniczenia[parametry.Faza.ALFA]._ruch, "y")

    def test_czy_ciecie(self):
        ograniczenie_test = parametry.Ograniczenia()
        oceny_alfa = [parametry.Ocena("a", 10), parametry.Ocena("b", 2)]
        oceny_beta = [parametry.Ocena("c", 5), parametry.Ocena("d", 7)]
        ograniczenia = [parametry.Ograniczenia(), parametry.Ograniczenia()]
        for ogr, par_ogr in zip(ograniczenia, zip(oceny_alfa, oceny_beta)):
            ogr_a, ogr_b = par_ogr
            ogr.aktualizuj(parametry.Faza.ALFA, ogr_a, "x")
            ogr.aktualizuj(parametry.Faza.BETA, ogr_b, "x")
        wlasciwe = [True, False]
        for ogr, wl_wyn in zip(ograniczenia, wlasciwe):
            wynik = ogr.czy_ciecie()
            self.assertEqual(wl_wyn, wynik)

    def test_czy_aktualizowac(self):
        rozpatrywane_fazy = [parametry.Faza.ALFA, parametry.Faza.ALFA,
                             parametry.Faza.BETA, parametry.Faza.BETA]
        ograniczenia = [parametry.Ograniczenia() for k in rozpatrywane_fazy]
        oceny_alfa = [parametry.Ocena("x", 10), parametry.Ocena("x", 5),
                      parametry.Ocena("x", 20), parametry.Ocena("x", 30)]
        oceny_beta = [parametry.Ocena("x", 13), parametry.Ocena("x", 14),
                      parametry.Ocena("x", -2), parametry.Ocena("x", -1)]
        oceny = [parametry.Ocena("x", 20), # 20 > 10
                 parametry.Ocena("x", 1), # 1 > 5 NIE !!!
                 parametry.Ocena("x", -3), # -3 < -2
                 parametry.Ocena("x", 1)] # 1 < -1 NIE !!!
        wlasciwe_wyniki = [True, False, True, False]
        for ogr, par_ogr in zip(ograniczenia, zip(oceny_alfa, oceny_beta)):
            ogr_a, ogr_b = par_ogr
            ogr.aktualizuj(parametry.Faza.ALFA, ogr_a, "x")
            ogr.aktualizuj(parametry.Faza.BETA, ogr_b, "x")
        for ogr, ocena, wl_wyn, faza in zip(ograniczenia, oceny,
                                            wlasciwe_wyniki,
                                            rozpatrywane_fazy):
                 wynik = ogr.czy_aktualizowac(faza, ocena)
                 self.assertEqual(wl_wyn, wynik)

def main():
    unittest.main()
if __name__ == "__main__":
    main()
