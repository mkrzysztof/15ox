import  pygame
import siatka
import zarzadca
import sys

#stałe
WIELKOSC = 20 # liczba pixeli przypadających na komórkę
POCZATEK = (50, 50)
    
pygame.init()

class Symbol_graf:
    """graficzna reprezentacja x lub o"""

    def rysuj_na_pozycji(self, pozycja, surface):
        poz_x = POCZATEK[1] + pozycja[1] * WIELKOSC + pozycja[1] + 1
        poz_y = POCZATEK[0] + pozycja[0] * WIELKOSC + pozycja[0] + 1
        surface.blit(self.sym, (poz_x, poz_y))
        pygame.display.flip()
    
    def __init__(self):
        self.font = pygame.font.SysFont("", 30)
        self.sym = None
        zarzadca.zarejestruj(self.__class__,self.rysuj_na_pozycji)

class Kolko_graf(Symbol_graf):    
    def __init__(self):
        super().__init__()
        self.sym = self.font.render('o', False, (0, 255, 0))


class Krzyzyk_graf(Symbol_graf):
    def __init__(self):
        super().__init__()
        self.sym = self.font.render('x', False, (0, 255, 0))

class Puste_graf(Symbol_graf):
    pass

def rysuj_siatke(plansza_rozmiar, surface):
    """ Rysuje plansze
    """
    wiersze, kolumny = plansza_rozmiar
    wielkosc_obszaru = (wiersze * WIELKOSC + wiersze + 1,
                        kolumny * WIELKOSC + kolumny + 1)
    obwodka = pygame.Rect((0, 0), wielkosc_obszaru)
    obwodka.move_ip(*POCZATEK)
    pygame.draw.rect(surface, (255, 0, 0), obwodka, 1)
    #rysowanie linii poziomych
    pozx_pocz = POCZATEK[0]
    pozx_koniec = pozx_pocz  + wiersze * WIELKOSC + wiersze
    y = POCZATEK[1] + WIELKOSC + 1
    for p in range(1, wiersze):
        pygame.draw.line(surface, (255, 0, 0),
                         (pozx_pocz, y), (pozx_koniec, y))
        y += WIELKOSC + 1
    pozy_pocz = POCZATEK[1]
    pozy_koniec = pozy_pocz + kolumny * WIELKOSC + kolumny
    x = POCZATEK[0] + WIELKOSC + 1
    for p in range(1, kolumny):
        pygame.draw.line(surface, (255, 0, 0),
                         (x, pozy_pocz), (x, pozy_koniec))
        x += WIELKOSC + 1
    pygame.display.flip()

def odczyt_poz_myszy():
    wyj = False
    zegar = pygame.time.Clock()
    while not wyj:
        poz = pygame.mouse.get_pos()
        poz = [poz[1] - POCZATEK[1], poz[0] - POCZATEK[0]]
        poz_w = [x // (WIELKOSC + 1) for x in poz]
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                wyj = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        zegar.tick(40)
    return siatka.Polozenie(*poz_w)


def wyswietl_gracza(gracz, surface):
    font = pygame.font.SysFont("", 40)
    gumka = pygame.Rect((400, 400),(600, 440))
    pygame.draw.rect(surface, pygame.color.THECOLORS['black'], gumka)
    pygame.display.flip()
    napis = font.render(gracz.nazwa, False, pygame.color.THECOLORS['green'])
    surface.blit(napis, (400, 400))
    pygame.display.flip()

zarzadca.zarejestruj('wyswietl-gracza', wyswietl_gracza)

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
                sys.exit(0)
