"""element który po kliknięciu w niego myszą zostaje na stałe włączony
wyłączyć go można jedynie z zewnątrz"""
import pygame
import zarzadca
import plansza_wyboru_mod as pwm

pygame.font.init()
WIELKOSC = 30
FONT = pygame.font.SysFont("", WIELKOSC)
KOLOR = pygame.color.THECOLORS["white"]
_ZAZNACZONY = pygame.image.load('zaznaczony.png')
ODZNACZONY = pygame.image.load('odznaczony.png')
OK = pygame.image.load('OK.png')


class Przycisk:
    """ogólna redprezentacja przycisku"""
    def dodaj_obsluge(self, komunikat, funkcja_zwrotna, *parametry):
        self.komunikat = komunikat
        if parametry:
            self.parametry = parametry
        zarzadca.zarejestruj(komunikat, funkcja_zwrotna)

    def __init__(self, komunikat=None, funkcja_zwrotna=None):
        self.komunikat = komunikat
        self.parametry = None
        self.zajmowany_obszar = None
        self.surface = None
        if komunikat is not None:
            self.dodaj_obsluge(komunikat, funkcja_zwrotna)

    def umiesc_na_pozycji(self, x, y, obrazek, surface):
        """umieszcza przycisk na pozycji (x, y) na powierzchni wskazywanej
        przez surface"""
        self.surface = surface
        self.zajmowany_obszar = pygame.Rect(x, y, *obrazek.get_size())
        self.surface.blit(ODZNACZONY, (x, y))
        pygame.display.flip()

    def czy_kliknieto(self, event):
        kliknieto = False
        zajmowany_obszar = self.zajmowany_obszar
        poz_myszy = pygame.mouse.get_pos()
        if (event.type == pygame.MOUSEBUTTONDOWN
            and zajmowany_obszar.collidepoint(poz_myszy)):
            kliknieto = True
        return kliknieto


class PrzyciskGraf:
    """graficzna reprezentacja elementu"""
    def __init__(self, komunikat=None, funkcja_zwrotna=None):
        """komunikat - komunikat wysyłany po zaznaczeniu pola"""
        self.przycisk = Przycisk(komunikat, funkcja_zwrotna)
        self.jest_aktywny = False #nie zaznaczone

    def dodaj_obsluge(self, komunikat, funkcja_zwrotna, *parametry):
        self.przycisk.dodaj_obsluge(komunikat, funkcja_zwrotna, *parametry)
        
    def umiesc_na_pozycji(self, x, y, surface):
        self.przycisk.umiesc_na_pozycji(x, y, _ZAZNACZONY, surface)
        
    def wyczysc(self):
        przycisk = self.przycisk
        zajmowany_obszar = przycisk.zajmowany_obszar
        pygame.draw.rect(przycisk.surface,
                         pygame.color.THECOLORS['black'],
                         zajmowany_obszar)
        pygame.display.flip()
        przycisk.surface.blit(ODZNACZONY, zajmowany_obszar.topleft)
        pygame.display.flip()
        print("wyczysc")
        self.jest_aktywny = False
        
    def wykryj_klikniecie(self, pygame_events):
        """wykrywa zaznaczernie pola jako argument przyjmuje
        listę zdarzeń pygame"""
        zajmowany_obszar = self.przycisk.zajmowany_obszar
        pozycja_pola = zajmowany_obszar.topleft
        for event in pygame_events:
            if (self.przycisk.czy_kliknieto(event) and not self.jest_aktywny):
                self.zaznacz()
                self.przycisk.surface.blit(_ZAZNACZONY, pozycja_pola)
                pygame.display.flip()
        
    def zaznacz(self):
        """zaznacza pole wyboru"""
        if not self.jest_aktywny:
            self.jest_aktywny = True
            przycisk = self.przycisk
            zarzadca.rozeslij(przycisk.komunikat, *przycisk.parametry)


class PrzyciskOK:
    def __init__(self):
        self.przycisk = Przycisk()
    
    """Przycisk zatwierdzający"""
    def dodaj_obsluge(self, komunikat, funkcja_zwrotna, *parametry):
        self.przycisk.dodaj_obsluge(komunikat, funkcja_zwrotna, *parametry)

    def umiesc_na_pozycji(self, x, y, surface):
        self.surface = surface
        self.przycisk.zajmowany_obszar = pygame.Rect(x, y, *OK.get_size())
        self.surface.blit(OK, (x, y))
        pygame.display.flip()

    def wykryj_klikniecie(self, pygame_events):
        for event in pygame_events:
            if self.przycisk.czy_kliknieto(event):
                pwm.zatwierdzono_wybor = True
        
