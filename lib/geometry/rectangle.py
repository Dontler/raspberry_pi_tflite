from lib.geometry.point import Point


class Rectangle:

    def __init__(self, p1: Point, p2: Point):
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2
