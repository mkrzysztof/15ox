import pygame
import zaznaczenie

def funkcja_zwrotna(drugi_przycisk):
    print("Zaznaczono")
    print(drugi_przycisk)
    if drugi_przycisk.reprezentacja:
        print("czyszczę drugi")
        drugi_przycisk.wyczysc()

def funkcja_zwrotna2(drugi_przycisk):
    print("Zaznaczono 2")

if __name__ == "__main__":
    SURFACE = pygame.display.set_mode((800, 600))
    przycisk = zaznaczenie.PrzyciskGraf()
    przycisk2 = zaznaczenie.PrzyciskGraf()
    przycisk.dodaj_obsluge("przycisk1", funkcja_zwrotna, przycisk2)
    przycisk2.dodaj_obsluge("przycisk2", funkcja_zwrotna, przycisk)
    przycisk.umiesc_na_pozycji(50, 50, SURFACE)
    przycisk2.umiesc_na_pozycji(50, 150, SURFACE)
    zegar = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        przycisk.wykryj_klikniecie(events)
        #zegar.tick(15)
        przycisk2.wykryj_klikniecie(events)
        #zegar.tick(15)
