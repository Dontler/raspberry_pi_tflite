class Point:

    def __init__(self, x, y):
        self._x = int(x)
        self._y = int(y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def to_tuple(self):
        return tuple((self._x, self._y))
