


class Plansza:
    def __init__(self, mapOfButtons):
        self._howMuchBombsIsMarked = 0
        self._mapOfButtons = mapOfButtons

    def flag(self, x, y):
        self._howMuchBombsIsMarked += 1
        self._mapOfButtons[y][x].dezaktywuj()
        self._mapOfButtons[y][x].mark("flag")