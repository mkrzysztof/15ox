""" przyciski radio """
import pygame

PIONOWY_ODSTEP = 50

def obsluga_radio(funkcje_obslugi, pola, aktywna_opcja):
    # aktywuje wybraną aktywną opcje, czyści przyciski nie związane
    # z tą opcją
    funkcje_obslugi[aktywna_opcja]()
    for k in (funkcje_obslugi.keys() - {aktywna_opcja}):
        pola[k].wyczysc()

# obsługa zgrupowanych pól

def _umiesc_radio(przyciski, pozycje, surface):
    opcje = przyciski.keys()
    for opcja, pozycja in zip(opcje, pozycje):
        przyciski[opcja].umiesc_na_pozycji(*pozycja, surface)

def _umiesc_napisy(pola_radio, pozycje_napisow, surface):
    opcje = pola_radio.keys()
    font = pygame.font.SysFont("", 30)
    for rozmiar, pozycja in zip(opcje, pozycje_napisow):
        napis = font.render(rozmiar, False, pygame.color.THECOLORS['green'])
        surface.blit(napis, pozycja)
    pygame.display.flip()

def _dolacz_obsluge(pola, funkcja_obslugi):
    opcje = pola.keys()
    for opcja in opcje:
        pola[opcja].dodaj_obsluge(opcja, funkcja_obslugi, opcja)

def utworz_radio(pola, funkcja_obslugi, pozycja, surface):
    """ tworzy zgrupowane pole wyboru typu 'radio' 
    Argumenty:
    pola -- lista pól radio indeksowana ich opisami
    funkcja_obslugi -- funkcja obsługująca utworzone pole radio
    pozycja -- pozycja na utworzonym oknie graficznym
    surface -- okno graficzne """
    poz_x, poz_y = pozycja
    pozycje_radio = [(poz_x, poz_y + i * PIONOWY_ODSTEP)
                         for i in range(len(pola))]
    _umiesc_radio(pola, pozycje_radio, surface)
    _dolacz_obsluge(pola, funkcja_obslugi)

def dodaj_napisy(pola, pozycja, surface):
    poz_x_napisu, poz_y_napisu = pozycja
    pozycje_napisow = [(poz_x_napisu, poz_y_napisu + i * PIONOWY_ODSTEP)
                       for i in range(len(pola))]
    _umiesc_napisy(pola, pozycje_napisow, surface)

def obsluz_radio(events, pola):
    for rozmiar, pole in pola.items():
        pole.wykryj_klikniecie(events)
