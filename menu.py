import tkinter
from tkinter import DISABLED


class Menu:
    def __init__(self, window):

        self._window = window

        self._zdjecieMenu = tkinter.PhotoImage(file='menu.png')
        self._tytul = tkinter.Label(self._window, image=self._zdjecieMenu)
        self._tytul.grid(row=0, columnspan=50, sticky="news")

        l0 = tkinter.Label(window, text='\n')
        l0.grid(column=1, row=1)

        self._szerokosc = tkinter.Label(self._window, text="X (szerokość)", bg='orange')
        self._szerokosc.grid(row=2, sticky="e")
        self._szerokosc = tkinter.Entry(self._window)
        self._szerokosc.grid(row=2, column=1)

        self._wysokosc = tkinter.Label(self._window, text="Y (wysokość)", bg='yellow')
        self._wysokosc.grid(row=3, sticky="e")
        self._wysokosc = tkinter.Entry(self._window)
        self._wysokosc.grid(row=3, column=1)

        self._miny = tkinter.Label(self._window, text="Miny (ilość min)", bg='pink')
        self._miny.grid(row=4, sticky="e")
        self._miny = tkinter.Entry(self._window)
        self._miny.grid(row=4, column=1)

        l0 = tkinter.Label(window, text='\n')
        l0.grid(column=2, row=5)

        l0 = tkinter.Label(window, text='\n')
        l0.grid(column=0, row=5)

        self._graj = tkinter.Button(self._window, text="GRAJ", bg='gray')
        self._graj.grid(columnspan=2)

        self._restart = tkinter.Button(self._window, text="RESET", stat=DISABLED, bg='red')
        self._restart.grid(columnspan=2)
