"""wizualna część plansza_wyboru"""
import pygame
import plansza_wyboru_mod as pwm
import zaznaczenie

#stałe
ROZMIAR = (800, 600)
POZ_Y_POCZATKOWA = 50
PIONOWY_ODSTEP = 50
rozmiary_planszy = ['xo', '10x10', '15x15',]
przyciski_zmian = {k : zaznaczenie.PrzyciskGraf() for k in rozmiary_planszy}
wybory_rozmiarow = [pwm.wybierz_xo, pwm.wybierz_10x10, pwm.wybierz_15x15]
fun_wyborow = dict(zip(rozmiary_planszy, wybory_rozmiarow))
przycisk_OK = zaznaczenie.PrzyciskOK()

# obsługa zgrupoowanych trzech przycisków
def funkcja_obslugi(rozmiar):
    fun_wyborow[rozmiar]()
    for k in (set(rozmiary_planszy) - {rozmiar}):
        przyciski_zmian[k].wyczysc()

def umiesc_przyciski(rozmiary_planszy, pozycje_przyc, surface):
    for rozmiar, pozycja in zip(rozmiary_planszy, pozycje_przyc):
        przyciski_zmian[rozmiar].umiesc_na_pozycji(*pozycja, surface)

def umiesc_napisy(rozmiary_planszy, pozycje_napisow, surface):
    font = pygame.font.SysFont("", 30)
    for rozmiar, pozycja in zip(rozmiary_planszy, pozycje_napisow):
        napis = font.render(rozmiar, False, pygame.color.THECOLORS['green'])
        surface.blit(napis, pozycja)
    pygame.display.flip()

def dolacz_obsluge(rozmiary_planszy, funkcja_obslugi):
    for rozmiar in rozmiary_planszy:
        przyciski_zmian[rozmiar].dodaj_obsluge(rozmiar, funkcja_obslugi,
                                               rozmiar)
def obsluz_przyciski(events, przyciski):
    for rozmiar, przycisk in przyciski.items():
        przycisk.wykryj_klikniecie(events)
        
def utworz_przyciski(surface):
    poz_x_przycisku = 50
    pozycje_przyc = [(poz_x_przycisku, POZ_Y_POCZATKOWA + i * PIONOWY_ODSTEP)
                     for i in range(len(rozmiary_planszy))]
    umiesc_przyciski(rozmiary_planszy, pozycje_przyc, surface)
    dolacz_obsluge(rozmiary_planszy, funkcja_obslugi)

def dodaj_napisy(surface):
    poz_x_napisu = 100
    pozycje_napisow = [(poz_x_napisu, POZ_Y_POCZATKOWA + i * PIONOWY_ODSTEP)
                       for i in range(len(rozmiary_planszy))]
    umiesc_napisy(rozmiary_planszy, pozycje_napisow, surface)


# przycisk OK

def funkcja_obslugi_OK():
    pwm.zatwierdzono_wybor = True

def wyswietl_OK(surface):
    przycisk_OK.umiesc_na_pozycji(200, 200, surface)
    przycisk_OK.dodaj_obsluge("OK", funkcja_obslugi_OK, None)

def obsloz_OK(events, przycisk_OK):
    przycisk_OK.wykryj_klikniecie(events)
        
def main():
    surface = pygame.display.set_mode(ROZMIAR)
    utworz_przyciski(surface)
    dodaj_napisy(surface)
    while True:
        events = pygame.event.get()
        obsluz_przyciski(events, przyciski_zmian)
    
if __name__ == "__main__":
    main()
    while True:
        pass
