from random import randint

from .greasy_phrases import greasy_phrases
from sessions import SessionStorage

class JokeGenerator:
    def __init__(self, session:SessionStorage):
        self.__session = session

    def pick_one(self):
        if not self.__session.jokes_available:
            self.__session.jokes_available = list(range(len(greasy_phrases)))
        lst = self.__session.jokes_available
        if len(lst) == 1:
            idx = lst.pop()
        if (length := len(lst)) > 1:
            idx = lst.pop(randint(0, length-1))
        self.__session.jokes_available = lst
        self.__session.save()
        return greasy_phrases[idx]