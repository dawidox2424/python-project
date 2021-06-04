from unittest import TestCase
from mapaGry import mapaGry
from plansza import Plansza
from saper import Saper
from window import Okno


class PlanszaTest(TestCase):
    def __init__(self, *args, **kwargs):
        """
        Tworzymy klasę PlanszaTest, która będzie wykorzystywana do przeprowadzenie testów jednostkowych
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        g = Saper()
        w = Okno(g)
        g.ustawWidok(w)
        wg = w.get_okno()
        g.setTestValues(8, 8, 12) #zgodnie z założeniami, rozmiar planszy to 8x8 a min jest 12

        self.winGame = mapaGry(wg, g)
        self.mapOfButtons = self.winGame.get_mapOfButtons(8, 8)
        self.board = Plansza(self.mapOfButtons)

    def testMarkedBombsIncreasedAfterSign(self):
        """
        Test sprawdza, czy po oznaczeniu pola na planszy, wzrasta licznik do liczenia oznaczonych pól
        """
        howMuchBombsIsMarkedBefore = self.board._howMuchBombsIsMarked
        self.board.flag(1, 1)
        howMuchBombsIsMarkedAfter = self.board._howMuchBombsIsMarked

        self.assertEqual(howMuchBombsIsMarkedBefore + 1, howMuchBombsIsMarkedAfter)

