import unittest
import unittest.mock as mock
import alfa_beta
import parametry
import siatka
import symbole


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

class TestAlfaBeta(unittest.TestCase):

    def test_alfa_beta_pelne(self):
        siatka_test = zbuduj_siatke(
            {
                symbole.Kolko:   [(0, 0), (1, 0), (2, 0)],
                symbole.Krzyzyk: [(0, 1), (0, 2)]
            }
        )
        ruch = siatka.Polozenie((2, 0))
        wlasciwy_wynik = 3
        stan_gry = parametry.StanGry(siatka=siatka_test, ostatni_ruch=ruch)
        gracz_a = mock.Mock()
        gracz_a.symbol = symbole.Kolko
        gracz_b = mock.Mock()
        gracz_b.symbol = symbole.Krzyzyk
        alfa_beta.inicjuj_graczy(gracz_a, gracz_b)
        oceny = parametry.nowe_ograniczenia()
        wynik = alfa_beta.alfa_beta(stan_gry, parametry.Faza.BETA, 0, oceny)
        self.assertNotEqual(wlasciwy_wynik, wynik._wartosc)

    def test_alfa_beta(self):
        siatka_test = zbuduj_siatke(
            {
                symbole.Kolko:   [(0, 0), (1, 0)],
                symbole.Krzyzyk: [(0, 1), (0, 2)]
            }
        )
        ruch = siatka.Polozenie((0, 0))
        wlasciwy_wynik1 = parametry.Ocena(siatka.Polozenie((2, 0)), -3)
        # taki ruch też maksymalizuje
        wlasciwy_wynik2 = parametry.Ocena(siatka.Polozenie((2, 0)), -3)
        stan_gry = parametry.StanGry(siatka=siatka_test, ostatni_ruch=ruch)
        gracz_a = mock.Mock()
        gracz_a.symbol = symbole.Kolko
        gracz_b = mock.Mock()
        gracz_b.symbol = symbole.Krzyzyk
        alfa_beta.inicjuj_graczy(gracz_a, gracz_b)
        oceny = parametry.nowe_ograniczenia()
        wynik = alfa_beta.alfa_beta(stan_gry, parametry.Faza.BETA, 0, oceny)
        wlasciwe_wyniki = [wlasciwy_wynik1, wlasciwy_wynik2]
        self.assertIn(wynik, wlasciwe_wyniki)

        


if __name__ == "__main__":
    unittest.main()
