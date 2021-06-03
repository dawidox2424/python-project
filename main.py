from saper import Saper
from window import Okno

if __name__ == '__main__':
    gra = Saper()
    oknoGry = Okno(gra)
    gra.ustawWidok(oknoGry)
    oknoGry.Loop()