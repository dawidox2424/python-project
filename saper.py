import random

import blad

class Saper:
    def __init__(self):
        """
        Główna klasa odpowiedzialna za obsługę całej gry (logika + wywołanie tworzenia mapy gry)
        """
        self._kod = ""
        self._wyczyszczonePola = 0
        self.koniecGry = False #zmienna, która "kontroluje" czy gra  nadal trwa czy powinna się już zakończyć
        self._pierwszeUruchomienie = False #zmienna do kontroli czy gra została włączona po raz pierwszy
        self._miny = 0
        self._oznaczoneMiny = 0
        self._dobrzeOznaczoneMiny = 0
        self._szerokoscMapy = 0
        self._wysokoscMapy = 0
        self._mapaMin = []

    def ustawWidok(self, widok):
        self._widok = widok


    def przycisk(self, znak):
        """
        Przycisk jest wykorzystywany przy wyrażeniu lambda w klasie Okno. Służy on do kontroli wciskanych przycisków.
        Również do obsługi kodu xyzzy (program musi "wykryć" że coś jest wpisywane i sprawdzić czy to na pewno kod xyzzy.
        """
        self._kod = znak + self._kod[0:5]
        self.xyzzy()

    def xyzzy(self):
        """
        Jedno z założeń programu (po wpisaniu na klawiaturze kodu "xyzzy" gra podpowiada gdzie znajdują się miny
        """
        if "xyzzy" in self._kod[::-1]:
            self._kod = ""
            self.pokazMiny(what="onlyColor")

    def nowaGra(self):
        """
        Tworzenie nowej gry. Najpierw zerowane są początkowe zmienne potrzebne do obsługi logiki gry, a następnie
        ustawiane są początkowe parametry, takie jak szerokość, wysokość, ilośc min itd.
        W razie niepowodzenia wyrzycany jest wyjątek.
        """
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
        """
        Ustawienie danych potrzebnych do wygenerowania mapy gry.
        Njapierw po przepisaniu zmiennych z getDaneWejsciowe ustawiane są parametry gry.
        Następnie sprawdzane są dane poprzez własny wyjątek (jeden z wymagań dodatkowych) który znajduję się w pliku
        blad.py.
        Jeżeli wszystkie dane są zgodne, następuje rysowanie mapy przez metodę rysujMapę()
        I rozpoczynana jest nowa gra.
        """
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
        """
        Czasami zachodzi konieczność pokazania wszystkich min (na przykład po wygraniu gry przez oflagowanie
        wszystkich pól z minami lub na przykład po przegranej - chcemy wtedy zobaczyć gdzie były miny)
        """
        for x in range(self._wysokoscMapy):
            for y in range(self._szerokoscMapy):
                if self._mapaMin[x][y][0] == "M":
                    self._widok.mapa.pokazMiejsceMiny(y, x, what)

    def rysujMape(self):
        """
        Używając random.sample możemy wylosować miejsca gdzie znajdują sie miny i wedle tego losowania je rozmieszczamy
        """
        losowo = random.sample(range(0, self._szerokoscMapy * self._wysokoscMapy), self._miny)
        self._mapaMin = [["Mn" if j * self._szerokoscMapy + i in losowo else "0n" for i in range(self._szerokoscMapy)]
                          for j in range(self._wysokoscMapy)]
        self._mapaMin = [["Mn" if self._mapaMin[j][i][0] == "M" else str(self.liczMinyObok(i, j)) + "n" for i in
                           range(self._szerokoscMapy)] for j in range(self._wysokoscMapy)]

    def liczMinyObok(self, x, y) -> int:
        """
        Metoda licząca ile jest min wokół danego miejsca (x,y)
        :param x: koordynata x
        :param y: koordynata y
        :return: licznik zwraca ilość min wokół danego miejsca
        """
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
        """
        Aby zresetować grę, najpierw należy ustawić wszystkie jej parametry do wartości poczatkowych.
        Następnie mapa jest resetowana i tworzona jest od nowa.
        :return:
        """
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
        """
        Lewym przyciskiem myszy możemy sprawdzić dane pole (odkryć je) w zależności od tego czy jest tam mina czy nie:
        - jeśli jest tam mina to przegrywamy grę i następuje koniec.
        - jeśli jest to puste pole, to zostaje ono odkryte + sprawdzane jest czy można "odkryć więcej" pól
        - po każdym odkryciu pola (czy też pól) sprawdzane jest czy przypadkiem gracz "już" nie wygrał danej rozgrywki

        :param x: pozycja x danego pola
        :param y: pozycja y danego pola
        """
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
        """
        Prawy przycisk myszy służy do oznaczania pól flagą lub pytajnikiem.
        W zależności od tego czy w danym miejscu jest mina czy nie, odpowiednie liczniki dotyczące
        ilości min dobrze oznaczonych i po prostu oznaczonych są aktualizowane.

        :param pos_x: pozycja pola x
        :param pos_y: pozycja pola y
        """
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
        """
        Metoda wykonywana jest w sytuacji gdy gracz naciśnie na puste pole, a w okół znajdują się inne puste pole,
        które też mogą zostać odkryte, przez co jednym kliknięciem można odsłonić większy fragment mapy gry.
        :param x: pozycja x pola
        :param y: pozycja y pola
        :return: odkryte  - zwraca ilośc pól jakie zostaną odkryte (w celu zaktualizowania licznika pól odkrytych,
        który musi posiadać tę informację, gdyż od niej zależy czy gra zostanie wygrana)
        """
        odkryte = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if y + i < 0 or x + j < 0 or self._mapaMin[y + i][x + j][1] == "f":
                        continue
                    elif self._mapaMin[y + i][x + j][1] in "nq":
                        odkryte += 1
                        self._mapaMin[y + i][x + j] = self._mapaMin[y + i][x + j][0] + "o"
                        self._widok.mapa.odkryjPrzycisk(x + j, y + i, int(self._mapaMin[y + i][x + j][0]))
                        if self._mapaMin[y + i][x + j][0] == "0":
                            odkryte += self.odkryjPustePola(x + j, y + i)
                except IndexError:
                    continue
        return odkryte

    def wygrana(self):
        """
        Metoda wygrana opisuje jakie warunki muszą zajść by daną rozgrywkę można uznać za wygraną.

        Mamy dwie możliwości:
            -albo gracz oznaczy wszystkie miny flagami (i tylko te pola - żadne inne!)
            -albo gracz "odkryje" wszystkie puste pole, gdzie nie znajdują się żadne miny
        """
        if self._miny == self._dobrzeOznaczoneMiny == self._oznaczoneMiny or \
                self._wyczyszczonePola == self._szerokoscMapy * self._wysokoscMapy - self._miny: #warunek wygrania gry
            self._koniecGry = True
            self._widok.mapa.wygrana()

    def setTestValues(self, height, width, mines):
        """
        Metoda wykorzystywana wyłącznie do testów jednostkowych.
        Ustawia ona przykładowe wartości początkowe, potrzebne do rozpoczęcia gry.
        Następnie na potrzeby testów generowana jest mapa gry.

        :param height: wysokość planszy
        :param width: szerokość plaszy
        :param mines: ilość min do rozmieszczenia
        """
        self._wysokoscMapy = height
        self._szerokoscMapy = width
        self._miny = mines
        self._oznaczoneMiny = 0
        self._dobrzeOznaczoneMiny = 0
        self._wyczyszczonePola = 0
        self._koniecGry = False
        if not 2 <= self._szerokoscMapy <= 15 or not 2 <= self._wysokoscMapy <= 15 or \
                not 0 <= self._miny <= self._szerokoscMapy * self._wysokoscMapy:
            raise Exception("BŁĘDNE DANE!")
        self.rysujMape()
