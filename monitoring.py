def pokaz_wywolanie(fun):
    """raportuje wuwołanie funkcjii do adnotacji"""
    def __opakowanie(*args, **kwds):
        print('wywołuję: ', fun.__name__)
        return fun(*args, **kwds)
    return __opakowanie
