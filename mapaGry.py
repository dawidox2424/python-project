import time
from tkinter import *

from przycisk import przycisk

class mapaGry:
    def __init__(self, okno, gra, pozycjax=3, pozycjay=1):
        """
        Klasa mapa gry jest odpowiedzialna za całą logikę związaną z planszą na której rozmieszczane są miny
        , mianowicie:
            - rysowanie przycisków
            - tworzenie nowej mapy
            - odkrywanie przycisków
            - oznaczanie przycisków (flaga, mina, pytajnik itd.)
            - zdefiniowanie wygranej i przegranej (komunikat + zatrzymanie zegara gry + odkrycie wszystkich pól)
            - definicja zegara gry + jego logika
        :rtype: mapaGry
        """
        self._gra = gra
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
        """
        Dodatkowa funkcjonalność - zegar liczący czas, jaki był potrzebny graczowi na ukończenie rozgrywki
        """
        if self._czas_start:
            self._Licznik.set(str("%3.1f" % (time.time() - self._time)))
        elif self._started:
            self._time = time.time()
            self._Licznik.set(str(0))
            self._czas_start = True
            self._started = False
        self._okno.after(100, self.zegar)

    def rysujPrzyciski(self, szerokosc, wysokosc):
        """
        Metoda wykorzystywana jest do tworzenia mapy przycisków (tylko gdy uruchamiana jest nowa gra).
        :param szerokosc: szerokość planszy
        :param wysokosc:  wysokość planszy
        """
        [[y.zniszcz() for y in x] for x in self._mapa_przycikow]
        self._mapa_przycikow = [[przycisk(self._okno, i, j, self._gra.lewyPrzyciskMyszy, self._gra.prawyPrzyciskMyszy,
                                     i + self._px, j + self._py + 1)
                             for i in range(szerokosc)] for j in range(wysokosc)]

    def nowa(self, height, width, miny):
        """
        Metoda tworzy nową mapę gry, ustawia parametr oznaczonych min na zero (bo to początek gry),
        następnie wywołuję metodę do tworzenia mapy przycisków (osobna metoda do tworzenia stricte mapa_przyciskow)
        :param height:  wysokość planszy
        :param width: szerokość planszy
        :param miny: ilość min
        """
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
        """
        Odkrywanie pustego przycisku (po odkryciu pozostaje nam puste pole - brak miny)
        :param x: koordynata x przycisku
        :param y: koordynata y przycisku
        :param number: numer tutaj jest zawsze "0"
        ponieważ odkrywamy tutaj puste pole (pod 0 jest zdjęcie pustego pola)
        """
        self._mapa_przycikow[y][x].odkryj(number)

    def wygrana(self):
        """
        Wyświetlenie komunikatu o wygranej + dezaktywacja wszystkich przycisków (nie można w nie kliknąć)
        """
        self._wygrana_przegrana.config(text="WYGRAŁEŚ! GRATULACJE!", bg="green")
        [[x.dezaktywuj() for x in y] for y in self._mapa_przycikow]
        self._czas_start = False

    def ustawPrzycisk(self, x, y, what):
        """
        W zależności od tego czy użytkownik oznaczył dane miejsce flagą lub pytajnikiem, zmienia się licznik
        liczący ilość oznaczonych min + jeżeli użytkownik oznaczył dane miejsce flagą to nie można w nie kliknać
        (zabezpieczenie przed przypadkowym kliknięciem we flagę pod którą może być mina).

        :param x: koordynata x przycisku
        :param y: koordynata y przycisku
        :param what: opis tego co chcemy zrobić (oznaczyć flagę, pytajnik lub z powrotem na empty)
        """
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
        """
        Metoda pokazuje mine (zdjęcie) na danym (y,x):
        - w przypadku użycia kodu xyzzy pokazywane jest tylko delikatne podświetlenie miny (podpowiedź)
        - w innym przypadku pokazywana jest mina normalnie

        :param x: parametr x (koordynata miny)
        :param y: parametr y (koordynata miny)
        :param what: zmienna która pokazuje czy użyto kodu xyzzy
        :return:
        """
        self._mapa_przycikow[y][x].mark(oznaczenie="highlight")
        if what != "onlyColor":
            self._mapa_przycikow[y][x].mark(oznaczenie="mine")

    def przegrana(self, x, y):
        """
        Metoda przegrana jest wywoływana, gdy gracz przegra rozgrywkę tj. kiedy wejdzie na minę.
        :param x: koordynata x miny
        :param y: koordynata y miny
        """
        self._wygrana_przegrana.config(text="NIESTETY PRZEGRAŁEŚ", bg="red")
        [[xx.dezaktywuj() for xx in yy] for yy in self._mapa_przycikow]
        self._mapa_przycikow[y][x].mark(oznaczenie="minered") #pokazywana jest mina na czerwono (ta przez którą przegraliśmy)
        self._czas_start = False

    def get_mapOfButtons(self, width, height):
        """
        Metoda wykorzystywana wyłącznie w celach testowych. Zwraca ona mapę przycisków potrzebną do dalszych testów.
        (wcześniej ją generuje na podstawie paremetrów wysokości i szerokości)
        """
        self.rysujPrzyciski(width, height)
        return self._mapa_przycikow