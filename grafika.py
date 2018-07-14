import  pygame

pygame.init()

class Parametry:
    wielkosc = 20 # liczba pixeli przypadających na komórkę
    poczatek = (50, 50)

class Symbol_graf:
    """graficzna reprezentacja x lub o"""
    font = pygame.font.SysFont("", 30)
    sym = None
    @classmethod
    def rysuj_na_pozycji(cls, pozycja, surface):
        poz_x = Parametry.poczatek[1] + pozycja[1] * Parametry.wielkosc +\
            pozycja[1] + 1
        poz_y = Parametry.poczatek[0] + pozycja[0] * Parametry.wielkosc +\
            pozycja[0] + 1
        surface.blit(cls.sym, (poz_x, poz_y))
        pygame.display.flip()
        

class Kolko_graf(Symbol_graf):
    sym = Symbol_graf.font.render('o', False, (0, 255, 0))

class Krzyzyk_graf(Symbol_graf):
    sym = Symbol_graf.font.render('x', False, (0, 255, 0))


class Puste_graf(Symbol_graf):
    pass

def rysuj_siatke(plansza_rozmiar, surface):
    """ Rysuje plansze
    """
    wiersze, kolumny = plansza_rozmiar
    wielkosc = Parametry.wielkosc
    wielkosc_obszaru = (wiersze * wielkosc + wiersze + 1,
                        kolumny * wielkosc + kolumny + 1)
    obwodka = pygame.Rect((0, 0), wielkosc_obszaru)
    obwodka.move_ip(*Parametry.poczatek)
    pygame.draw.rect(surface, (255, 0, 0), obwodka, 1)
    #rysowanie linii poziomych
    pozx_pocz = Parametry.poczatek[0]
    pozx_koniec = pozx_pocz  + wiersze * wielkosc + wiersze
    y = Parametry.poczatek[1] + wielkosc + 1
    for p in range(1, wiersze):
        pygame.draw.line(surface, (255, 0, 0),
                         (pozx_pocz, y), (pozx_koniec, y))
        y += wielkosc + 1
    pozy_pocz = Parametry.poczatek[1]
    pozy_koniec = pozy_pocz + kolumny * wielkosc + kolumny
    x = Parametry.poczatek[0] + wielkosc + 1
    for p in range(1, kolumny):
        pygame.draw.line(surface, (255, 0, 0),
                         (x, pozy_pocz), (x, pozy_koniec))
        x += wielkosc + 1
    pygame.display.flip()

def odczyt_poz_myszy():
    wyj = False
    while not wyj:
        poz = pygame.mouse.get_pos()
        poz = [poz[1] - Parametry.poczatek[1], poz[0] - Parametry.poczatek[0]]
        poz_w = [x // (Parametry.wielkosc + 1) for x in poz]
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                wyj = True
    return poz_w


if __name__ == "__main__":
    surface = pygame.display.set_mode((800, 600))
    plansza_rozmiar = (15, 15)
    rysuj_siatke(plansza_rozmiar, surface)
    Krzyzyk_graf.rysuj_na_pozycji((10, 10), surface)
    Kolko_graf.rysuj_na_pozycji((0, 8), surface)
    pygame.display.flip()
    while True:
        odczyt_poz_myszy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
