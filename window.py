import tkinter
from menu import Menu
from mapaGry import mapaGry


class Okno:
    def __init__(self, gra):
        """
        Klasa okno tworzy nam okienko gry przy użyciu biblioteki tkinter
        :param gra: Gra to po prostu obiekt klasy Saper, ktory musimy przekazać do Okna, by wygenerować pełną grę
        """
        self._okno = tkinter.Tk()
        self._gra = gra
        # ustawiam parametry Window (okienko gry)
        self._okno.title("Minesweeper")
        self._okno.iconbitmap("ikona_gry.ico")  # ikonka gry .ico

        size_x = (self._okno.winfo_screenwidth() / 4)
        size_y = (self._okno.winfo_screenheight() / 4)
        self._okno.geometry('+%d+%d' % (size_x, size_y))

        self._okno.bind("<Key>", lambda klik: gra.przycisk(klik.char)) #użycie lambdy

        self.menu = Menu(self._okno, gra) #tworzymy Menu gry
        self.mapa = mapaGry(self._okno, gra) #tworzymy mapę gry
        self.mapa.zegar() #tworzenie zegara odliczającego czas od 0.0

    def Loop(self):
        """
        Metoda Loop() "utrzymuje" nasze okienko przy życiu, przez co cały czas widzimy je na ekranie
        """
        self._okno.mainloop()

    def get_okno(self):
        """
        Metoda używana jest do pobierania okienka gry (np. do celów testowania)
        :rtype: zwraca okno gry
        """
        return self._okno
