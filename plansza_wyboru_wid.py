"""Wizualna część plansza_wyboru"""
import pygame
import plansza_wyboru_mod as pwm
import zaznaczenie
import radio_wid

#stałe

_POZ_Y_POCZATKOWA = 50
_ROZMIARY_PLANSZY = ['xo', '10x10', '15x15',]
PRZYCISKI_ZMIAN = {k : zaznaczenie.PrzyciskGraf() for k in _ROZMIARY_PLANSZY}
_WYBORY_ROZMIAROW = [pwm.wybierz_xo, pwm.wybierz_10x10, pwm.wybierz_15x15]
_FUN_WYBOROW = dict(zip(_ROZMIARY_PLANSZY, _WYBORY_ROZMIAROW))

_KTO_GRA = ['GRACZ - GRACZ', 'KOMPUTER - GRACZ', 'GRACZ - KOMPUTER']
PRZYCISKI_KTO_GRA = {k: zaznaczenie.PrzyciskGraf() for k in _KTO_GRA}
_WYBOR_KTO_GRA = [pwm.wybierz_gracz_gracz, pwm.wybierz_komputer_gracz,
                 pwm.wybierz_gracz_komputer]
_FUN_KTO_GRA = dict(zip(_KTO_GRA, _WYBOR_KTO_GRA))

PRZYCISK_OK = zaznaczenie.PrzyciskOK()

def utworz_pole_radio(pola_radio, poz_x, funkcja_obslugi, surface):
    ODSTEP = 70
    pozycja = (poz_x, _POZ_Y_POCZATKOWA)
    radio_wid.utworz_radio(pola_radio, funkcja_obslugi,
                           pozycja, surface)
    pozycja = (poz_x + ODSTEP, _POZ_Y_POCZATKOWA)
    radio_wid.dodaj_napisy(pola_radio, pozycja, surface)

def _funkcja_obslugi_roz(rozmiar):
    radio_wid.obsluga_radio(_FUN_WYBOROW, PRZYCISKI_ZMIAN, rozmiar)
        
def utworz_przyciski_rozm(surface):
    utworz_pole_radio(PRZYCISKI_ZMIAN, 50, _funkcja_obslugi_roz, surface)
        
# przyciski wybór ilości

def _funkcja_obslugi_ile(kto):
    radio_wid.obsluga_radio(_FUN_KTO_GRA, PRZYCISKI_KTO_GRA, kto)

def utworz_przyciski_ile(surface):
    utworz_pole_radio(PRZYCISKI_KTO_GRA, 180, _funkcja_obslugi_ile, surface)
    

# przycisk OK

def _funkcja_obslugi_OK():
    pwm.zatwierdzono_wybor = True

def wyswietl_OK(surface):
    PRZYCISK_OK.umiesc_na_pozycji(200, 200, surface)
    PRZYCISK_OK.dodaj_obsluge("OK", _funkcja_obslugi_OK, None)

def obsloz_OK(events, PRZYCISK_OK):
    PRZYCISK_OK.wykryj_klikniecie(events)
