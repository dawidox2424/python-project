import tkinter
from tkinter import DISABLED, ACTIVE


class Menu:
    def __init__(self, window, ster):
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
        self._blad = tkinter.Label(self._window, text="", fg="red")

        l0 = tkinter.Label(window, text='\n', height = 1)
        l0.grid(column=2, row=6)

        l0 = tkinter.Label(window, text='\n',height = 1)
        l0.grid(column=0, row=7)

        self._graj = tkinter.Button(self._window, text="GRAJ", bg='gray')
        self._graj.grid(columnspan=2)

        self._restart = tkinter.Button(self._window, text="RESET", stat=DISABLED, bg='red')
        self._restart.grid(columnspan=2)

        self._graj.bind("<Button-1>", lambda event: ster.nowaGra())
        self._graj.bind("<Return>", lambda event: ster.nowaGra())
        self._restart.bind("<Button-1>", lambda event: ster.restartGry())
        self._restart.bind("<Return>", lambda event: ster.restartGry())


    def startNowaGra(self):
        self._blad.grid_forget()
        self._restart.config(stat=ACTIVE)

    def errorDisplay(self, comment):
        self._blad.config(text=comment)
        self._blad.grid(row=6, columnspan=2)

    def getEntryData(self):
        return self._szerokosc.get(), self._wysokosc.get(), self._miny.get()
