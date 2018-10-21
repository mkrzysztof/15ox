""" moduł odpowiedzialny za wyświetlanie planszy końcowej """
import pygame
import zarzadca

def pokaz_wygrana(remis, biezacy_gracz, surface):
    font = pygame.font.SysFont("", 30)
    napis_wygrana = "WYGRAŁ "
    if biezacy_gracz.wygrana:
        kto = biezacy_gracz.nazwa
        napis_wygrana = napis_wygrana + kto
    elif remis:
        napis_wygrana = "REMIS"
    napis = font.render(napis_wygrana, False, pygame.color.THECOLORS['red'])
    surface.blit(napis, (100, 100))
    pygame.display.flip()
    
zarzadca.zarejestruj('pokaz-wygrana', pokaz_wygrana)
