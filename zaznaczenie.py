"""element który po kliknięciu w niego myszą zostaje na stałe włączony
wyłączyć go można jedynie z zewnątrz"""
import pygame
import zarzadca

pygame.font.init()
WIELKOSC = 30
FONT = pygame.font.SysFont("", WIELKOSC)
KOLOR = pygame.color.THECOLORS["white"]
ZAZNACZONY = pygame.image.load('zaznaczony.png')
ODZNACZONY = pygame.image.load('odznaczony.png')

class PrzyciskGraf:
    """graficzna reprezentacja elementu"""

    def dodaj_obsluge(self, komunikat, funkcja_zwrotna, parametr = None):
        self.komunikat = komunikat
        self.parametr = parametr
        zarzadca.zarejestruj(komunikat, funkcja_zwrotna)
    
    def __init__(self, komunikat=None, funkcja_zwrotna=None):
        """komunikat - komunikat wysyłany po zaznaczeniu pola"""
        self.reprezentacja = False #nie zaznaczone
        self.zajmowany_obszar = None
        self.surface = None
        if komunikat is not None:
            self.dodaj_obsluge(komunikat, funkcja_zwrotna)

    def umiesc_na_pozycji(self, x, y, surface):
        """umieszcza przycisk na pozycji (x, y) na powierzchni wskazywanej
        przez surface"""
        self.surface = surface
        self.zajmowany_obszar = pygame.Rect(x, y, *ODZNACZONY.get_size())
        self.surface.blit(ODZNACZONY, (x, y))
        pygame.display.flip()

    def wyczysc(self):
        pygame.draw.rect(self.surface, pygame.color.THECOLORS['black'],
                         self.zajmowany_obszar)
        pygame.display.flip()
        self.surface.blit(ODZNACZONY, self.zajmowany_obszar.topleft)
        pygame.display.flip()
        print("wyczysc")
        self.reprezentacja = False
        
    def wykryj_klikniecie(self, pygame_events):
        """wykrywa zaznaczernie pola jako argument przyjmuje
        listę zdarzeń pygame"""
        zajmowany_obszar = self.zajmowany_obszar
        poz_myszy = pygame.mouse.get_pos()
        pozycja_pola = zajmowany_obszar.topleft
        for event in pygame_events:
            if (event.type == pygame.MOUSEBUTTONDOWN
                and zajmowany_obszar.collidepoint(poz_myszy)
                and not self.reprezentacja):
                self.zaznacz()
                #self.wyczysc()
                self.surface.blit(ZAZNACZONY, pozycja_pola)
                pygame.display.flip()
        
    def zaznacz(self):
        """zaznacza pole wyboru"""
        if not self.reprezentacja:
            self.reprezentacja = True
            zarzadca.rozeslij(self.komunikat, self.parametr)
