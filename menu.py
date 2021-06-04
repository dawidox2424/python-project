import tkinter
from tkinter import DISABLED, ACTIVE


class Menu:
    def __init__(self, okno, gra):
        """
        Klasa Menu służy do wygenerowania pól potrzebnych do wprowadzenia danych takich jak:
            - szerokość mapy
            - długość mapy
            - ilość min
        :param okno: Paremetr okno
        :param gra: Parametr gry
        """
        self._okno = okno

        self._zdjecieMenu = tkinter.PhotoImage(file='menu.png')
        self._tytul = tkinter.Label(self._okno, image=self._zdjecieMenu)
        self._tytul.grid(row=0, columnspan=50, sticky="news")

        l0 = tkinter.Label(okno, text='\n')
        l0.grid(column=1, row=1)

        self._szerokosc = tkinter.Label(self._okno, text="X (szerokość)", bg='orange')
        self._szerokosc.grid(row=2, sticky="e")
        self._szerokosc = tkinter.Entry(self._okno)
        self._szerokosc.grid(row=2, column=1)

        self._wysokosc = tkinter.Label(self._okno, text="Y (wysokość)", bg='yellow')
        self._wysokosc.grid(row=3, sticky="e")
        self._wysokosc = tkinter.Entry(self._okno)
        self._wysokosc.grid(row=3, column=1)

        self._miny = tkinter.Label(self._okno, text="Miny (ilość min)", bg='pink')
        self._miny.grid(row=4, sticky="e")
        self._miny = tkinter.Entry(self._okno)
        self._miny.grid(row=4, column=1)
        self._blad = tkinter.Label(self._okno, text="", fg="red")

        l0 = tkinter.Label(okno, text='\n', height = 1)
        l0.grid(column=2, row=6)

        l0 = tkinter.Label(okno, text='\n',height = 1)
        l0.grid(column=0, row=7)

        self._graj = tkinter.Button(self._okno, text="GRAJ", bg='gray')
        self._graj.grid(columnspan=2)

        self._restart = tkinter.Button(self._okno, text="RESET", stat=DISABLED, bg='red')
        self._restart.grid(columnspan=2)

        self._graj.bind("<Button-1>", lambda event: gra.nowaGra())
        self._graj.bind("<Return>", lambda event: gra.nowaGra())
        self._restart.bind("<Button-1>", lambda event: gra.restartGry())
        self._restart.bind("<Return>", lambda event: gra.restartGry())


    def startNowaGra(self):
        """
        Metoda start uruchamia nową grę (konfiguracja widgeta)
        """
        self._blad.grid_forget()
        self._restart.config(stat=ACTIVE)

    def errorDisplay(self, comment):
        self._blad.config(text=comment)
        self._blad.grid(row=6, columnspan=2)

    def getDaneWejsciowe(self):
        return self._szerokosc.get(), self._wysokosc.get(), self._miny.get()
