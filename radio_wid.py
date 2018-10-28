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

def _umiesc_radio(opcje, przyciski, pozycje, surface):
    for opcja, pozycja in zip(opcje, pozycje):
        przyciski[opcja].umiesc_na_pozycji(*pozycja, surface)

def _umiesc_napisy(opcje, pozycje_napisow, surface):
    font = pygame.font.SysFont("", 30)
    for rozmiar, pozycja in zip(opcje, pozycje_napisow):
        napis = font.render(rozmiar, False, pygame.color.THECOLORS['green'])
        surface.blit(napis, pozycja)
    pygame.display.flip()

def _dolacz_obsluge(opcje, pola, funkcja_obslugi):
    for opcja in opcje:
        pola[opcja].dodaj_obsluge(opcja, funkcja_obslugi, opcja)

def utworz_radio(opcje, pola, funkcja_obslugi,
                     poz_x, poz_y, surface):
    """ tworzy zgrupowane pole wyboru typu 'radio' 
    Argumenty:
    opcje -- lista opisów
    pola -- lista pól typu PrzyciskiGraf
    funkcja_obslugi -- funkcja obsługująca utworzone pole radio
    poz_x, poz_y -- pozycja na utworzonym oknie graficznym
    surface -- okno graficzne """
    pozycje_radio = [(poz_x, poz_y + i * PIONOWY_ODSTEP)
                         for i in range(len(opcje))]
    _umiesc_radio(opcje, pola, pozycje_radio, surface)
    _dolacz_obsluge(opcje, pola, funkcja_obslugi)

def dodaj_napisy(pozycja, opcje, surface):
    poz_x_napisu, poz_y_napisu = pozycja
    pozycje_napisow = [(poz_x_napisu, poz_y_napisu + i * PIONOWY_ODSTEP)
                       for i in range(len(opcje))]
    _umiesc_napisy(opcje, pozycje_napisow, surface)

def obsluz_radio(events, pola):
    for rozmiar, pole in pola.items():
        pole.wykryj_klikniecie(events)
