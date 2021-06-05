from saper import Saper
from window import Okno
"""
Main - służy do włączenia gry:
- najpierw tworzymy obiekt klasy Saper
- następnie na jego podstawie tworzymy okno gry
- następnie do atrybutu klasy Saper o nazwie widok, przypisujemy widok = oknoGry (wcześniej już utworzone)
- na koniec wywołujemy metodę klasy Okno, która "utrzymuje" nasze okienko na ekranie dzięki metodzie mainlook (tkinter)
"""
if __name__ == '__main__':
    gra = Saper()
    oknoGry = Okno(gra)
    gra.ustawWidok(oknoGry)
    oknoGry.Loop()


