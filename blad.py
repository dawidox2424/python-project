
class zledane(Exception):
    def __init__(self, komentarz):
        self.komentarz = komentarz

    def __str__(self):
        return self.komentarz