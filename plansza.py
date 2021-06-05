
class Plansza:
    def __init__(self, mapOfButtons):
        """
        Klasa plansza została stworzona wyłącznie w celach testów jednostkowych
        :param mapOfButtons: czyli mapa przycisków (ich rozmiesczenie na mapie gry)
        """
        self._howMuchBombsIsMarked = 0
        self._mapOfButtons = mapOfButtons

    def flag(self, x, y):
        """
        Metoda flag, służy do sprawdzania czy licznik ilości zaznaczonych bomb wzrośnie, po oznaczeniu jedego z pól
        """
        self._howMuchBombsIsMarked += 1
        self._mapOfButtons[y][x].dezaktywuj()
        self._mapOfButtons[y][x].mark("flag")