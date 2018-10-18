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
KTO_GRA = ['GRACZ - GRACZ', 'KOMPUTER - GRACZ', 'GRACZ - KOMPUTER']
PRZYCISKI_KTO_GRA = {k: zaznaczenie.PrzyciskGraf() for k in KTO_GRA}
WYBOR_KTO_GRA = [pwm.wybierz_gracz_gracz, pwm.wybierz_komputer_gracz,
                 pwm.wybierz_gracz_komputer]
FUN_KTO_GRA = dict(zip(KTO_GRA, WYBOR_KTO_GRA))

def _obsluga_radio(funkcje_obslugi, przyciski, aktywna_opcja):
    # aktywuje wybraną aktywną opcje, czyści przyciski nie związane
    # z tą opcją
    funkcje_obslugi[aktywna_opcja]()
    for k in (funkcje_obslugi.keys() - {aktywna_opcja}):
        przyciski[k].wyczysc()

# obsługa zgrupowanych trzech przycisków
def _funkcja_obslugi_roz(rozmiar):
    _obsluga_radio(FUN_WYBOROW, PRZYCISKI_ZMIAN, rozmiar)

def _funkcja_obslugi_ile(kto):
    _obsluga_radio(FUN_KTO_GRA, PRZYCISKI_KTO_GRA, kto)

def _umiesc_radio(opcje, przyciski, pozycje, surface):
    for opcja, pozycja in zip(opcje, pozycje):
        przyciski[opcja].umiesc_na_pozycji(*pozycja, surface)

def _umiesc_napisy(ROZMIARY_PLANSZY, pozycje_napisow, surface):
    font = pygame.font.SysFont("", 30)
    for rozmiar, pozycja in zip(ROZMIARY_PLANSZY, pozycje_napisow):
        napis = font.render(rozmiar, False, pygame.color.THECOLORS['green'])
        surface.blit(napis, pozycja)
    pygame.display.flip()

def _umiesc_przyciski_ile(ROZMIARY_PLANSZY, pozycje_przyc, surface):
    pass

def _dolacz_obsluge(opcje, przyciski, funkcja_obslugi):
    for opcja in opcje:
        przyciski[opcja].dodaj_obsluge(opcja, funkcja_obslugi, opcja)

def _dolacz_obsluge_ile(ROZMIARY_PLANSZY, _funkcja_obslugi):
    pass

def obsluz_przyciski_rozm(events, przyciski):
    for rozmiar, przycisk in przyciski.items():
        przycisk.wykryj_klikniecie(events)

def obsluz_przyciski_ile(events, przyciski):
    for rozmiar, przycisk in przyciski.items():
        przycisk.wykryj_klikniecie(events)
        
def utworz_przyciski_rozm(surface):
    poz_x_przycisku = 50
    pozycje_przyc = [(poz_x_przycisku, POZ_Y_POCZATKOWA + i * PIONOWY_ODSTEP)
                     for i in range(len(ROZMIARY_PLANSZY))]
    _umiesc_radio(ROZMIARY_PLANSZY, PRZYCISKI_ZMIAN, pozycje_przyc, surface)
    _dolacz_obsluge(ROZMIARY_PLANSZY, PRZYCISKI_ZMIAN, _funkcja_obslugi_roz)

def dodaj_napisy_rozm(surface):
    poz_x_napisu = 100
    pozycje_napisow = [(poz_x_napisu, POZ_Y_POCZATKOWA + i * PIONOWY_ODSTEP)
                       for i in range(len(ROZMIARY_PLANSZY))]
    _umiesc_napisy(ROZMIARY_PLANSZY, pozycje_napisow, surface)


# przycisk OK

def _funkcja_obslugi_OK():
    pwm.zatwierdzono_wybor = True

def wyswietl_OK(surface):
    PRZYCISK_OK.umiesc_na_pozycji(200, 200, surface)
    PRZYCISK_OK.dodaj_obsluge("OK", _funkcja_obslugi_OK, None)

def obsloz_OK(events, PRZYCISK_OK):
    PRZYCISK_OK.wykryj_klikniecie(events)
        
# przyciski wybór ilości

def utworz_przyciski_ile(surface):
    poz_x_przycisku = 120
    pozycje_przyc = [(poz_x_przycisku, POZ_Y_POCZATKOWA + i * PIONOWY_ODSTEP)
                     for i in range(len(KTO_GRA))]
    _umiesc_radio(KTO_GRA, PRZYCISKI_KTO_GRA, pozycje_przyc, surface)
    _dolacz_obsluge(KTO_GRA, PRZYCISKI_KTO_GRA, _funkcja_obslugi_ile)

def dodaj_napisy_ile(surface):
    poz_x_napisu = 250
    pozycje_napisow = [(poz_x_napisu, POZ_Y_POCZATKOWA + i * PIONOWY_ODSTEP)
                       for i in range(len(KTO_GRA))]
    _umiesc_napisy(KTO_GRA, pozycje_napisow, surface)


if __name__ == "__main__":
    def main():
        surface = pygame.display.set_mode(ROZMIAR)
        utworz_przyciski(surface)
        dodaj_napisy(surface)
        while True:
            events = pygame.event.get()
            obsluz_przyciski(events, PRZYCISKI_ZMIAN)

    main()
    while True:
        pass
