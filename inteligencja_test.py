import inteligencja
import siatka
import gracz
import symbol


gracz1 = gracz.GraczCzlowiek(symbol.Kolko)
gracz2 = gracz.GraczCzlowiek(symbol.Krzyzyk)
gracz1.przeciwnik = gracz2
gracz2.przeciwnik = gracz1
gracz1.mnoznik = -1
gracz2.mnoznik = 1
siatka_poczatkowa = siatka.Siatka(3, 3)
wzor = ['.o.',
        '...',
        '...',]
siatka_poczatkowa.wypelnij_siatke(wzor)

ostatni_ruch = siatka.Polozenie(0, 1)

drzewo = inteligencja.buduj_drzewo(siatka_poczatkowa, gracz2)
k, l = inteligencja.min_max(drzewo, gracz2)
print(k, l)
