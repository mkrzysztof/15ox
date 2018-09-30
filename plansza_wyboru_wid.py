"""wizualna część plansza_wyboru"""
import pygame
import plansza_wyboru_mod as pwm
import zaznaczenie

#stałe
ROZMIAR = (800, 600)
klucze_rozmiar = ['xo', '10x10', '15x15',]
wybor_rozmiaru = {k : zaznaczenie.PrzyciskGraf() for k in klucze_rozmiar}
zaznaczenia = [pwm.wybierz_xo, pwm.wybierz_10x10, pwm.wybierz_15x15]
fun_zazn = dict(zip(klucze_rozmiar, zaznaczenia))

def funkcja_obslugi(kl):
    fun_zazn[kl]()
    for k in (set(klucze_rozmiar) - {kl}):
        wybor_rozmiaru[k].wyczysc()
        
def main():
    surface = pygame.display.set_mode(ROZMIAR)
    pozycje = [(50, 50), (50, 100), (50, 150)]
    for kl, poz in zip(klucze_rozmiar, pozycje):
        wybor_rozmiaru[kl].dodaj_obsluge(kl, funkcja_obslugi, kl)
        wybor_rozmiaru[kl].umiesc_na_pozycji(*poz, surface)
    while True:
        events = pygame.event.get()
        for kl in klucze_rozmiar:
            wybor_rozmiaru[kl].wykryj_klikniecie(events)
    
if __name__ == "__main__":
    main()
    while True:
        pass
