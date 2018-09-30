""" zarządzająca zdarzeniami """
fun_zwrotne = {}

def zarejestruj(komunikat, funkcja_zwrotna):
    fun_zwrotne[komunikat] = funkcja_zwrotna

def rozeslij(komunikat, *parametr):
    fun_zwrotne[komunikat](*parametr)
        

    
