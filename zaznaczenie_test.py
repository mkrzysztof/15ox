import pygame
import zaznaczenie

def funkcja_zwrotna(drugi_przycisk, trzeci_przycisk):
    print("Zaznaczono")
    print(drugi_przycisk)
    if drugi_przycisk.reprezentacja or trzeci_przycisk.reprezentacja:
        print("czyszczę drugi")
        drugi_przycisk.wyczysc()
        trzeci_przycisk.wyczysc()

if __name__ == "__main__":
    SURFACE = pygame.display.set_mode((800, 600))
    przycisk1 = zaznaczenie.PrzyciskGraf()
    przycisk2 = zaznaczenie.PrzyciskGraf()
    przycisk3 = zaznaczenie.PrzyciskGraf()
    przycisk1.dodaj_obsluge("przycisk1", funkcja_zwrotna, przycisk2, przycisk3)
    przycisk2.dodaj_obsluge("przycisk2", funkcja_zwrotna, przycisk1, przycisk3)
    przycisk3.dodaj_obsluge("przycisk2", funkcja_zwrotna, przycisk1, przycisk2)
    przycisk1.umiesc_na_pozycji(50, 50, SURFACE)
    przycisk2.umiesc_na_pozycji(50, 150, SURFACE)
    przycisk3.umiesc_na_pozycji(50, 200, SURFACE)
    zegar = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        przycisk1.wykryj_klikniecie(events)
        przycisk2.wykryj_klikniecie(events)
        przycisk3.wykryj_klikniecie(events)
