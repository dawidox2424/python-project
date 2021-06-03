import random

import blad


class Saper:
    def __init__(self):
        self._kod = ""
        self._wyczyszczonePola = 0
        self.koniecGry = False
        self._pierwszeUruchomienie = False
        self._miny = 0
        self._oznaczoneMiny = 0
        self._dobrzeOznaczoneMiny = 0
        self._szerokoscMapy = 0
        self._wysokoscMapy = 0
        self._mapaMin = []

    def ustawWidok(self, widok):
        self._widok = widok


    def przycisk(self, znak):
        self._kod = znak + self._kod[0:5]
        self.xyzzy()

    def xyzzy(self):
        if "xyzzy" in self._kod[::-1]:
            self._kod = ""
            self.pokazMiny(what="onlyColor")

    def nowaGra(self):
        self._oznaczoneMiny = 0
        self._dobrzeOznaczoneMiny = 0
        self._wyczyszczonePola = 0
        self._koniecGry = False
        try:
            self.ustawDane()
        except ValueError:
            self._widok.menu.errorDisplay("Dane są niepoprawne!!!")
        except blad.zledane:
            self._widok.menu.errorDisplay("Podałeś złe wymiary lub błędną ilość min do rozstawienia!")

    def ustawDane(self):
        self._szerokoscMapy, self._wysokoscMapy, self._miny = self._widok.menu.getDaneWejsciowe()

        self._szerokoscMapy = int(self._szerokoscMapy)
        self._wysokoscMapy = int(self._wysokoscMapy)
        self._miny = int(self._miny)
        if not 2 <= self._szerokoscMapy <= 15 or not 2 <= self._wysokoscMapy <= 15 or \
                not 0 <= self._miny <= self._szerokoscMapy * self._wysokoscMapy:
            raise blad.zledane("")
        self._widok.mapa.nowa(self._wysokoscMapy, self._szerokoscMapy, self._miny)
        self.rysujMape()
        self._widok.menu.startNowaGra()
        self._pierwszeUruchomienie = True

    def pokazMiny(self, what=""):
        for x in range(self._wysokoscMapy):
            for y in range(self._szerokoscMapy):
                if self._mapaMin[x][y][0] == "M":
                    self._widok.mapa.pokazMiejsceMiny(y, x, what)

    def rysujMape(self):
        losowo = random.sample(range(0, self._szerokoscMapy * self._wysokoscMapy), self._miny)
        self._mapaMin = [["Mn" if j * self._szerokoscMapy + i in losowo else "0n" for i in range(self._szerokoscMapy)]
                          for j in range(self._wysokoscMapy)]
        self._mapaMin = [["Mn" if self._mapaMin[j][i][0] == "M" else str(self.liczMinyObok(i, j)) + "n" for i in
                           range(self._szerokoscMapy)] for j in range(self._wysokoscMapy)]

    def liczMinyObok(self, x, y) -> int:
        licznik = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i + y < 0 or j + x < 0:
                    continue
                try:
                    if self._mapaMin[i + y][j + x][0] == "M":
                        licznik += 1
                except IndexError:
                    continue
        return licznik

    def restartGry(self):
        if self._pierwszeUruchomienie:
            self._oznaczoneMiny = 0
            self._dobrzeOznaczoneMiny= 0
            self._wyczyszczonePola = 0
            self._koniecGry = False
            for i in range(self._wysokoscMapy):
                for j in range(self._szerokoscMapy):
                    self._mapaMin[i][j] = self._mapaMin[i][j][0] + "n"
            self._widok.mapa.nowa(self._wysokoscMapy, self._szerokoscMapy, self._miny)

    def lewyPrzyciskMyszy(self, x, y):
        if self._mapaMin[y][x][0] == "M":
            self._koniecGry = True
            self.pokazMiny()
            self._widok.mapa.przegrana(x, y)
        else:
            if self._mapaMin[y][x][0] == "0":
                self._wyczyszczonePola += self.odkryjPustePola(x, y)
            else:
                self._wyczyszczonePola += 1
                self._widok.mapa.odkryjPrzycisk(x, y, int(self._mapaMin[y][x][0]))
            self._mapaMin[y][x] = self._mapaMin[y][x][0] + "o"
            self.wygrana()

    def prawyPrzyciskMyszy(self, pos_x, pos_y):
        if not self._koniecGry and self._mapaMin[pos_y][pos_x][1] != "o":
            if self._mapaMin[pos_y][pos_x][1] == "f":
                self._oznaczoneMiny -= 1
                self._mapaMin[pos_y][pos_x] = self._mapaMin[pos_y][pos_x][0] + "q"
                if self._mapaMin[pos_y][pos_x][0] == "M":
                    self._dobrzeOznaczoneMiny -= 1
                self._widok.mapa.ustawPrzycisk(pos_x, pos_y, "questionmark")
            elif self._mapaMin[pos_y][pos_x][1] == "q":
                self._mapaMin[pos_y][pos_x] = self._mapaMin[pos_y][pos_x][0] + "n"
                self._widok.mapa.ustawPrzycisk(pos_x, pos_y, "empty")
            else:
                self._mapaMin[pos_y][pos_x] = self._mapaMin[pos_y][pos_x][0] + "f"
                self._oznaczoneMiny += 1
                if self._mapaMin[pos_y][pos_x][0] == "M":
                    self._dobrzeOznaczoneMiny += 1
                self._widok.mapa.ustawPrzycisk(pos_x, pos_y, "flag")
            self.wygrana()

    def odkryjPustePola(self, x, y):
        nieodkryte = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if y + i < 0 or x + j < 0 or self._mapaMin[y + i][x + j][1] == "f":
                        continue
                    elif self._mapaMin[y + i][x + j][1] in "nq":
                        nieodkryte += 1
                        self._mapaMin[y + i][x + j] = self._mapaMin[y + i][x + j][0] + "o"
                        self._widok.mapa.odkryjPrzycisk(x + j, y + i, int(self._mapaMin[y + i][x + j][0]))
                        if self._mapaMin[y + i][x + j][0] == "0":
                            nieodkryte += self.odkryjPustePola(x + j, y + i)
                except IndexError:
                    continue
        return nieodkryte

    def wygrana(self):
        if self._miny == self._dobrzeOznaczoneMiny == self._oznaczoneMiny or \
                self._wyczyszczonePola == self._szerokoscMapy * self._wysokoscMapy - self._miny:
            self._koniecGry = True
            self._widok.mapa.wygrana()