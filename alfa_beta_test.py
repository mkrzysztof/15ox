import unittest
import gracz
import gracz_komputer
import alfa_beta
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

    def test_czy_to_koniec(self):
        # lista danych testowych
        # pojedyńcza dana to lista:
        # [ słownik_opisany_w_zbuduj_siatke,
        #   położenie,
        #   etap
        #   wartość_oczekiwana]
        dane_testowe = [
            [
                zbuduj_siatke(
                    {
                        symbole.Kolko:   [(0, 0), (0, 2), (1, 1), (2, 1)],
                        symbole.Krzyzyk: [(0, 1), (1, 0), (1, 2), (2, 0), (2, 2)]
                    }
                ),
                siatka.Polozenie((0, 0)),
                "ALFA",
                True,
            ],
            [
                zbuduj_siatke(
                    {
                        symbole.Kolko: [(0, 0), (1, 1)],
                        symbole.Krzyzyk: [(0, 2)]
                    }
                ),
                siatka.Polozenie((1, 1)),
                "ALFA",
                False,
            ],
        ]
        for dane in dane_testowe:
            siatka_test, polozenie, etap, wlasciwy_wynik = dane
            wynik = alfa_beta.czy_to_koniec(siatka_test, polozenie, etap, 0)
            self.assertEqual(wlasciwy_wynik, wynik)

    def test_czy_to_koniec_poziom_lim(self):
        siatka_test = zbuduj_siatke(
            {
                symbole.Kolko: [(0, 0), (1, 1)],
                symbole.Krzyzyk: [(0, 2)]
            }
        )
        ruch = siatka.Polozenie((0, 0))
        wlasciwy_wynik = True
        wynik = alfa_beta.czy_to_koniec(siatka_test, ruch, "ALFA", 7)
        self.assertEqual(wlasciwy_wynik, wynik)

    def test_czy_to_koniec_wygrana(self):
        siatka_test = zbuduj_siatke(
            {
                symbole.Kolko:   [(0, 0), (0, 1), (0, 2)],
                symbole.Krzyzyk: [(1, 0), (1, 1), (2, 0)]
            }
        )
        ruch = siatka.Polozenie((0, 1))
        wlasciwy_wynik = True
        wynik = alfa_beta.czy_to_koniec(siatka_test, ruch, "BETA", 3)
        self.assertEqual(wlasciwy_wynik, wynik)

    def test_alfa_beta_pelne(self):
        siatka_test = zbuduj_siatke(
            {
                symbole.Kolko:   [(0, 0), (1, 0), (2, 0)],
                symbole.Krzyzyk: [(0, 1), (0, 2)]
            }
        )
        gracz_komputerowy = gracz_komputer.GraczKomputer(symbole.Kolko)
        ruch = siatka.Polozenie((2, 0))
        wlasciwy_wynik = -3
        ocena_alfa = alfa_beta.OcenaRuchu()
        ocena_alfa.ocena = - 100
        ocena_beta = alfa_beta.OcenaRuchu()
        ocena_beta.ocena = 100
        oceny = {"ALFA": ocena_alfa, "BETA": ocena_beta}
        wynik = alfa_beta.alfa_beta(siatka_test, ruch,
                                    oceny, 0, "BETA")
        self.assertNotEqual(wlasciwy_wynik, wynik.ocena)

    def test_alfa_beta(self):
        siatka_test = zbuduj_siatke(
            {
                symbole.Kolko:   [(0, 0), (1, 0)],
                symbole.Krzyzyk: [(0, 1), (0, 2)]
            }
        )
        gracz_czlowiek = gracz.GraczCzlowiek(symbole.Krzyzyk)
        gracz_komputerowy = gracz_komputer.GraczKomputer(symbole.Kolko)
        ruch = siatka.Polozenie((0, 2))
        wlasciwy_wynik = alfa_beta.OcenaRuchu()
        wlasciwy_wynik.ocena = 3
        wlasciwy_wynik.ruch = siatka.Polozenie((2, 0))
        ocena_alfa = alfa_beta.OcenaRuchu()
        ocena_alfa.ocena = - 100
        ocena_beta = alfa_beta.OcenaRuchu()
        ocena_beta.ocena = 100
        oceny = {"ALFA": ocena_alfa, "BETA": ocena_beta}
        wynik = alfa_beta.alfa_beta(siatka_test, ruch,
                                    oceny, 0, "ALFA")
        self.assertEqual(wlasciwy_wynik, wynik)
        

if __name__ == "__main__":
    unittest.main()
