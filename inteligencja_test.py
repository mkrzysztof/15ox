import inteligencja
import siatka
import gracz


gracz1 = gracz.GraczCzlowiek('x')
gracz2 = gracz.GraczCzlowiek('o')
gracz1.przeciwnik = gracz2
gracz2.przeciwnik = gracz1
gracz1.mnoznik = 1
gracz2.mnoznik = -1
siatka_poczatkowa = siatka.Siatka(45, 45)
ruchy = [(siatka.Polozenie(0, 0), 'o'), (siatka.Polozenie(1, 0), 'x'),
         (siatka.Polozenie(0, 1), 'o'), (siatka.Polozenie(2, 0), 'x'),
         (siatka.Polozenie(1, 1), 'o'), (siatka.Polozenie(1, 3), 'x'),]
for r, sym in ruchy:
    siatka_poczatkowa.zapis_polozenie(r, sym)

ostatni_ruch = ruchy[-1][0]

drzewo = inteligencja.buduj_drzewo(siatka_poczatkowa, ostatni_ruch, gracz1)
k, l = inteligencja.min_max(drzewo, gracz1)
