import unittest
import alfa_beta
import siatka
import gracz
import gracz_komputer
import symbole
import wartosciowanie

class TestSiatki(unittest.TestCase):
    polozenia = [
        {
            "KOLKO": [(0, 0), (0, 2),],
            "KRZYZYK": [(1, 1),],
            "KONCOWA": (0, 2)
        },
        ]

    def __init__(self):
        self.czlowiek = gracz.GraczCzlowiek(symbole.Kolko)
        self.komputer = gracz_komputer.GraczKomputer(symbole.Krzyzyk)

    def stworz_stan_gry(self, polozenie):
        biez_siatka = siatka.Siatka(3, 3)
        # postaw kólka człowieka
        pozycje = polozenie["KOLKO"]
        for poz in pozycje:
            polozenie_ = siatka.Polozenie(poz)
            biez_siatka[polozenie_] = symbole.Kolko
        pozycje = polozenie["KRZYZYK"]
        for poz in pozycje:
            polozenie_ = siatka.Polozenie(poz)
            biez_siatka[polozenie_] = symbole.Krzyzyk
        return {"siatka": biez_siatka,
                "ostatni_ruch": siatka.Polozenie(polozenie["KONCOWA"])}

    def testowanie(self):
        for p in self.polozenia:
            stan_gry = self.stworz_stan_gry(p)
            print(stan_gry)
            ograniczenie = {"alfa": -100, "beta": 100}
            wynik = alfa_beta.alfa_beta(stan_gry, 0, ograniczenie,
                                        wartosciowanie.max_strony,
                                        siatka.otoczenie, "alfa")
            print(wynik)

t = TestSiatki()
t.testowanie()
