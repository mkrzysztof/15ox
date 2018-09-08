""" zarządzająca zdarzeniami """
fun_zwrotne = {}

def zarejestruj(klasa, funkcja_zwrotna):
    fun_zwrotne[klasa] = funkcja_zwrotna

def rozeslij(parametr, powierzchnia, komunikat):
    fun_zwrotne[komunikat.__class__](powierzchnia, parametr)
        

    
