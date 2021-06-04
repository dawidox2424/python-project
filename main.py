from unittest import TestCase

from blad import zledane
from mapaGry import mapaGry
from plansza import Plansza
from saper import Saper
from window import Okno

if __name__ == '__main__':
    gra = Saper()
    oknoGry = Okno(gra)
    gra.ustawWidok(oknoGry)
    oknoGry.Loop()


class PlanszaTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        g = Saper()
        w = Okno(g)  # Dodać przekazywanie rozmiaru planszy 8x8 i 12 min i powinno śmigać
        g.ustawWidok(w)
        wg = w.get_okno()
        g.setTestValues(8, 8, 12)

        self.winGame = mapaGry(wg, g)
        self.mapOfButtons = self.winGame.get_mapOfButtons(8, 8)
        self.board = Plansza(self.mapOfButtons)

    def testMarkedBombsIncreasedAfterSign(self):
        howMuchBombsIsMarkedBefore = self.board._howMuchBombsIsMarked
        self.board.flag(1, 1)
        howMuchBombsIsMarkedAfter = self.board._howMuchBombsIsMarked

        self.assertEqual(howMuchBombsIsMarkedBefore + 1, howMuchBombsIsMarkedAfter)

