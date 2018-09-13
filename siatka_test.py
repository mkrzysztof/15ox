import siatka
wierszy = 3
kolumn = 3

def test_wolne_pola():
    siatka1 = siatka.Siatka(wierszy, kolumn)
    for p in siatka1.wolne_pola():
        print(p, end=', ')


if __name__ == "__main__":
    test_wolne_pola()
