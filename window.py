import tkinter
from menu import Menu
from mapaGry import mapaGry


class Okno:
    def __init__(self, sterowanie):
        self._okno = tkinter.Tk()
        self._ster = sterowanie
        # ustawiam parametry Window (okienko gry)
        self._okno.title("Minesweeper")
        self._okno.iconbitmap("ikona_gry.ico")  # ikonka gry .ico

        size_x = (self._okno.winfo_screenwidth() / 4)
        size_y = (self._okno.winfo_screenheight() / 4)
        self._okno.geometry('+%d+%d' % (size_x, size_y))

        self._okno.bind("<Key>", lambda klik: sterowanie.przycisk(klik.char))

        self.menu = Menu(self._okno, sterowanie)
        self.mapa = mapaGry(self._okno, sterowanie)
        self.mapa.zegar()

    def Loop(self):
        self._okno.mainloop()  # petla "utrzymujaca" okienko
