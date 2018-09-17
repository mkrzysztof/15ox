import siatka
import unittest

siatka = siatka.Siatka(3, 3)
wzor1 = ['xox',
        '...',
        'xox',]
wzor2 = ['xxx',
         'ooo'
         'xxx',]

def testuj(siatka, wzor):
    siatka.wypelnij_siatke(wzor1)
    repr = []
    for wiersz in siatka.pola:
        pom = []
        for sym in wiersz:
            pom.append(sym.repr)
    repr.append("".join(pom))
    rowne = True
    for linia1, linia2 in zip(repr, wzor1):
        rowne = rowne and (linia1 == linia2)
    return rowne

class SiatkaTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(testuj(siatka, wzor1), True)
        

if __name__ == "__main__":
    unittest.main()
    

