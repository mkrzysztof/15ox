"""wizualna część plansza_wyboru"""
import pygame
import plansza_wyboru_mod as pwm
import zaznaczenie

#stałe
ROZMIAR = (800, 600)
POZ_Y_POCZATKOWA = 50
PIONOWY_ODSTEP = 50
ROZMIARY_PLANSZY = ['xo', '10x10', '15x15',]
PRZYCISKI_ZMIAN = {k : zaznaczenie.PrzyciskGraf() for k in ROZMIARY_PLANSZY}
WYBORY_ROZMIAROW = [pwm.wybierz_xo, pwm.wybierz_10x10, pwm.wybierz_15x15]
FUN_WYBOROW = dict(zip(ROZMIARY_PLANSZY, WYBORY_ROZMIAROW))
PRZYCISK_OK = zaznaczenie.PrzyciskOK()

# obsługa zgrupoowanych trzech przycisków
def funkcja_obslugi(rozmiar):
    FUN_WYBOROW[rozmiar]()
    for k in (set(ROZMIARY_PLANSZY) - {rozmiar}):
        PRZYCISKI_ZMIAN[k].wyczysc()

def umiesc_przyciski(ROZMIARY_PLANSZY, pozycje_przyc, surface):
    for rozmiar, pozycja in zip(ROZMIARY_PLANSZY, pozycje_przyc):
        PRZYCISKI_ZMIAN[rozmiar].umiesc_na_pozycji(*pozycja, surface)

def umiesc_napisy(ROZMIARY_PLANSZY, pozycje_napisow, surface):
    font = pygame.font.SysFont("", 30)
    for rozmiar, pozycja in zip(ROZMIARY_PLANSZY, pozycje_napisow):
        napis = font.render(rozmiar, False, pygame.color.THECOLORS['green'])
        surface.blit(napis, pozycja)
    pygame.display.flip()

def dolacz_obsluge(ROZMIARY_PLANSZY, funkcja_obslugi):
    for rozmiar in ROZMIARY_PLANSZY:
        PRZYCISKI_ZMIAN[rozmiar].dodaj_obsluge(rozmiar, funkcja_obslugi,
                                               rozmiar)
def obsluz_przyciski(events, przyciski):
    for rozmiar, przycisk in przyciski.items():
        przycisk.wykryj_klikniecie(events)
        
def utworz_przyciski(surface):
    poz_x_przycisku = 50
    pozycje_przyc = [(poz_x_przycisku, POZ_Y_POCZATKOWA + i * PIONOWY_ODSTEP)
                     for i in range(len(ROZMIARY_PLANSZY))]
    umiesc_przyciski(ROZMIARY_PLANSZY, pozycje_przyc, surface)
    dolacz_obsluge(ROZMIARY_PLANSZY, funkcja_obslugi)

def dodaj_napisy(surface):
    poz_x_napisu = 100
    pozycje_napisow = [(poz_x_napisu, POZ_Y_POCZATKOWA + i * PIONOWY_ODSTEP)
                       for i in range(len(ROZMIARY_PLANSZY))]
    umiesc_napisy(ROZMIARY_PLANSZY, pozycje_napisow, surface)


# przycisk OK

def funkcja_obslugi_OK():
    pwm.zatwierdzono_wybor = True

def wyswietl_OK(surface):
    PRZYCISK_OK.umiesc_na_pozycji(200, 200, surface)
    PRZYCISK_OK.dodaj_obsluge("OK", funkcja_obslugi_OK, None)

def obsloz_OK(events, PRZYCISK_OK):
    PRZYCISK_OK.wykryj_klikniecie(events)
        
def main():
    surface = pygame.display.set_mode(ROZMIAR)
    utworz_przyciski(surface)
    dodaj_napisy(surface)
    while True:
        events = pygame.event.get()
        obsluz_przyciski(events, PRZYCISKI_ZMIAN)
    
if __name__ == "__main__":
    main()
    while True:
        pass
<
