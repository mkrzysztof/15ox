import drzewo
import unittest

def buduj_drzewo():
    korzen = drzewo.Wezel('a1','et1', None)
    wezel1 = drzewo.Wezel('a2', 'et2', None)
    wezel2 = drzewo.Wezel('a3', 'et3', None)
    wezel3 = drzewo.Wezel('a4', 'et4', None)
    korzen['e1'] = wezel1
    korzen['e2'] = wezel2
    korzen['e3'] = wezel3
    print(list(korzen.keys()))
    return korzen

class ProstyTest(unittest.TestCase):
    def test1(self):
        drzewo = buduj_drzewo()
        pod1 = drzewo['e2']
        self.assertEqual('a3', pod1.stan_siatki)


if __name__ == "__main__":
    unittest.main()
