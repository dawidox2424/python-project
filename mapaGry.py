import time
from tkinter import *

from przycisk import przycisk

class mapaGry:

    def __init__(self, okno, ster, pozycjax=3, pozycjay=1):
        self._ster = ster
        self._px = pozycjax
        self._py = pozycjay
        self._okno = okno
        self._mapa_przycikow = []
        self._oznaczoneMiny = 0

        self._started = False
        self._czas_start = False
        self._time = time.time()

        self._flagaImg = PhotoImage(file='obrazki/flaga.png')
        self._MinaImg = PhotoImage(file='obrazki/mina.png')

        self._oznaczoneMinyMapa_text = StringVar()
        self._liczbaMinText = StringVar()
        self._Licznik = StringVar()
        self._Licznik.set("0")

        self._wygrana_przegrana = Label(self._okno, text="white")
        self._puste = Label(self._okno, image='', width="2")
        self._oznaczoneMinyMapa = Label(self._okno, textvariable=self._oznaczoneMinyMapa_text)
        self._oznaczoneMinyMapaIkona = Label(self._okno, image=self._flagaImg)
        self._labelMiny = Label(self._okno, textvariable=self._liczbaMinText)
        self._minyIkona = Label(self._okno, image=self._MinaImg)
        self._labelzegar = Label(self._okno, textvariable=self._Licznik)

    def zegar(self):
        if self._czas_start:
            self._Licznik.set(str("%3.1f" % (time.time() - self._time)))
        elif self._started:
            self._time = time.time()
            self._Licznik.set(str(0))
            self._czas_start = True
            self._started = False
        self._okno.after(100, self.zegar)

    def rysujPrzyciski(self, szerokosc, wysokosc):
        [[y.zniszcz() for y in x] for x in self._mapa_przycikow]
        self._mapa_przycikow = [[przycisk(self._okno, i, j, self._ster.lewyPrzyciskMyszy, self._ster.prawyPrzyciskMyszy,
                                     i + self._px, j + self._py + 1)
                             for i in range(szerokosc)] for j in range(wysokosc)]

    def nowa(self, height, width, miny):
        self._oznaczoneMiny = 0
        self._liczbaMinText.set(str(miny))

        self._oznaczoneMinyMapa_text.set(": 0")

        self._wygrana_przegrana.config(text="", bg="white")
        self._wygrana_przegrana.grid(column=self._px, row=self._py, columnspan=width, sticky="news")
        self._labelzegar.grid(column=self._px + width + 1, row=self._py, columnspan=2)

        self._puste.grid(column=width + self._px + 1, row=self._py + 1, rowspan=2)

        self._minyIkona.grid(column=width + self._px + 2, row=self._py + 1)
        self._labelMiny.grid(column=width + self._px + 3, row=self._py + 1)

        self._oznaczoneMinyMapaIkona.grid(column=width + self._px + 2, row=self._py + 2)
        self._oznaczoneMinyMapa.grid(column=width + self._px + 3, row=self._py + 2)
        self.rysujPrzyciski(width, height)
        self._started = True
        self._czas_start = False

    def odkryjPrzycisk(self, x, y, number):
        self._mapa_przycikow[y][x].odkryj(number)

    def wygrana(self):
        self._wygrana_przegrana.config(text="WYGRAŁEŚ! GRATULACJE!", bg="green")
        [[x.dezaktywuj() for x in y] for y in self._mapa_przycikow]
        self._czas_start = False

    def ustawPrzycisk(self, x, y, what):
        if what == "questionmark":
            self._oznaczoneMiny -= 1
            self._mapa_przycikow[y][x].aktywuj()
            self._mapa_przycikow[y][x].mark("questionmark")
        elif what == "empty":
            self._mapa_przycikow[y][x].mark("empty")
        elif what == "flag":
            self._oznaczoneMiny += 1
            self._mapa_przycikow[y][x].dezaktywuj()
            self._mapa_przycikow[y][x].mark("flag")
        self._oznaczoneMinyMapa_text.set(": " + str(self._oznaczoneMiny))

    def pokazMiejsceMiny(self, x, y, what=""):
        self._mapa_przycikow[y][x].mark(oznaczenie="highlight")
        if what != "onlyColor":
            self._mapa_przycikow[y][x].mark(oznaczenie="mine")

    def przegrana(self, x, y):
        self._wygrana_przegrana.config(text="NIESTETY PRZEGRAŁEŚ", bg="red")
        [[xx.dezaktywuj() for xx in yy] for yy in self._mapa_przycikow]
        self._mapa_przycikow[y][x].mark(oznaczenie="minered")
        self._czas_start = False

    def get_mapOfButtons(self, width, height):
        self.rysujPrzyciski(width, height)
        return self._mapa_przycikow