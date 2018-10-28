""" przyciski radio """

PIONOWY_ODSTEP = 50

def _obsluga_radio(funkcje_obslugi, pola, aktywna_opcja):
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

def obsluz_przyciski(events, pola):
    for rozmiar, przycisk in pola.items():
        przycisk.wykryj_klikniecie(events)

def utworz_radio(opcje, przyciski, funkcja_obslugi,
                     poz_x, poz_y, surface):
    pozycje_radio = [(poz_x, poz_y + i * PIONOWY_ODSTEP)
                         for i in range(len(opcje))]
    _umiesc_radio(opcje, przyciski, pozycje_radio, surface)
    _dolacz_obsluge(opcje, przyciski, funkcja_obslugi)
