from tkinter import *


class przycisk:
    def __init__(self, okno, i, j, LMB, RMB, x, y):
        """
        Klasa przycisku definiuje jego rozmiary, odpowiednie przypisanie zdjęć, w zależności od rodzaju przycisku np.:
        - mina
        - flaga
        - pytajnika
        - liczba z ilością min wokół
        :param okno: okno gry
        :param i: zmienna pomocnicza
        :param j: zmienna pomicnicza
        :param LMB: obsługa lewego przycisku myszy
        :param RMB: obsługa prawego przycisku myszy
        :param x: koordynata przycisku x
        :param y: koordynata przycisku y
        """
        self.okno = okno
        self.x = x
        self.y = y
        self.pytajnik_zdjecie = PhotoImage(file='obrazki/pytajnik.png')
        self.mina_zdjecie = PhotoImage(file='obrazki/mina.png')
        self.mina2_zdjecie = PhotoImage(file='obrazki/mina2.gif')
        self.flaga_zdjecie = PhotoImage(file='obrazki/flaga.png')
        self.liczby_zdjecia = {0: PhotoImage(file='obrazki/pusty.png'),
                               1: PhotoImage(file='obrazki/jeden.png'), 2: PhotoImage(file='obrazki/dwa.png'),
                               3: PhotoImage(file='obrazki/trzy.png'), 4: PhotoImage(file='obrazki/cztery.png'),
                               5: PhotoImage(file='obrazki/piec.png'), 6: PhotoImage(file='obrazki/szesc.png'),
                               7: PhotoImage(file='obrazki/siedem.png'), 8: PhotoImage(file='obrazki/osiem.png')}
        self.puste_zdjecie = PhotoImage(file='obrazki/pusty2.png')

        self.przycisk = Button(self.okno, bg='gray75', disabledforeground="black", relief=RAISED, overrelief=GROOVE,
                                 width=32, image=self.puste_zdjecie, command=(lambda a=i, b=j: LMB(a, b)))
        self.przycisk.bind("<Button-3>", lambda event, a=i, b=j: RMB(a, b)) #wykorzystanie lambdy (prawy przycisk myszy)
        self.przycisk.grid(row=y, column=x, sticky="news", padx=0, pady=0)

    def odkryj(self, liczba=0):
        """
        Okrycie przycisku pod którym może znajdować się liczba przedstawiająca ilość min w pobliżu.
        """
        self.przycisk.destroy()
        self.przycisk = Label(image=self.liczby_zdjecia[liczba], bg="grey85", width=32, height=32)
        self.przycisk.grid(row=self.y, column=self.x, sticky="news")

    def mark(self, oznaczenie="empty"):
        """
        :param oznaczenie: przekazywany jest tutaj rodzaj zaznaczenia jaki użytkownik chce wykonać:
            - minered ("wybuch" miny - gdy gracz przegra)
            - mine (zdjęcie miny)
            - highlight (podświetlenie pól gdzie znajdują się miny - użycie kodu xyzzy)
            - flag (ustawienie zdjęcia flagi na przycisku)
            - questionmark (ustwienie pytajnika na przycisku)
            - empty (cofnięcie się do stanu domyślnego - po prostu zwykły przycisk)
        """
        if oznaczenie == "minered":
            self.przycisk.destroy()
            self.przycisk = Label(image=self.mina2_zdjecie, width=32, height=32)
        elif oznaczenie == "mine":
            self.przycisk.destroy()
            self.przycisk = Label(image=self.mina_zdjecie, width=32, height=32)
        elif oznaczenie == "highlight":
            self.przycisk.config(bg="grey65")
        elif oznaczenie == "flag":
            self.przycisk.config(image=self.flaga_zdjecie)
        elif oznaczenie == "questionmark":
            self.przycisk.config(image=self.pytajnik_zdjecie)
        elif oznaczenie == "empty":
            self.przycisk.config(image=self.puste_zdjecie)
        self.przycisk.grid(row=self.y, column=self.x, sticky="news")

    def dezaktywuj(self):
        """
        Metoda do dezaktywacji przycisku (brak możliwości klikania)
        """
        self.przycisk.config(stat=DISABLED)

    def aktywuj(self):
        """
        Metoda do aktywacji przycisku (możliwość klikania)
        """
        self.przycisk.config(stat=ACTIVE)

    def zniszcz(self):
        """
        Metoda do usuwania przycisku (destroy).
        """
        self.przycisk.destroy()