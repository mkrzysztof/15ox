""" zarządzająca zdarzeniami """
fun_zwrotne = {}

def zarejestruj(klasa, funkcja_zwrotna):
    fun_zwrotne[klasa] = funkcja_zwrotna

def rozeslij(komunikat, *parametr):
    fun_zwrotne[komunikat.__class__](*parametr)
        

    
