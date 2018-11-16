import inteligencja
import siatka
import gracz
import drzewo
import unittest as ut

class TestInteligencja(ut.TestCase):
    def test_stworz_wierzcholek_przeciwnika(self):
        siatka1 = siatka.Siatka(10, 10)
        gr1 = gracz.GraczCzlowiek("x")
        gr2 = gracz.GraczCzlowiek("o")
        gr1.przeciwnik = gr2
        gr2.przeciwnik = gr1
        w1 = drzewo.Wierzcholek(siatka1, gr1)
        ruch = siatka.Polozenie((0,0))
        w2 = inteligencja.stworz_wierzcholek_przeciwnika(w1, ruch)
        self.assertEqual(gr2, w2.gracz)
        self.assertEqual("o", w2.siatka[ruch])

    def test_wartosciuj_wierzcholek(self):
        siatka1 = siatka.Siatka(10, 10)
        gr1 = gracz.GraczCzlowiek("x")
        gr2 = gracz.GraczCzlowiek("o")
        ruch = siatka.Polozenie((0,0))
        gr1.przeciwnik = gr2
        gr2.przeciwnik = gr1
        w1 = drzewo.Wierzcholek(siatka1, gr1)
        w2 = inteligencja.dodaj_ruch_na_siatce(w1, ruch)
        inteligencja.wartosciuj_wierzcholek(w2, ruch)
        self.assertEqual(None, w2.wartosc)

    def test_wartosciuj_wierzcholek_zap(self):
        # test całkowicie zapełnionego wierzchołka
        w = 3
        k = 3
        siatka_t = siatka.Siatka(w, k)
        gr1 = gracz.GraczCzlowiek("x")
        gr2 = gracz.GraczCzlowiek("o")
        gr1.przeciwnik = gr2
        gr2.przeciwnik = gr1
        w = drzewo.Wierzcholek(siatka_t, gr1)
        ruchy = {(siatka.Polozenie((0,0)), gr1),
                 (siatka.Polozenie((0,1)), gr2),
                 (siatka.Polozenie((0,2)), gr2),
                 (siatka.Polozenie((1,0)), gr2),
                 (siatka.Polozenie((1,1)), gr2),
                 (siatka.Polozenie((1,2)), gr1),
                 (siatka.Polozenie((2,0)), gr1),
                 (siatka.Polozenie((2,1)), gr1),
                 (siatka.Polozenie((2,2)), gr2),}
        for ruch, gr in ruchy:
            w.siatka[ruch] = gr.symbol
        inteligencja.wartosciuj_wierzcholek(w, siatka.Polozenie((2,0)))
        wartosc = w.wartosc
        self.assertEqual(0, wartosc)

if __name__ == "__main__":
    ut.main()
