from lib.geometry.point import Point


class Label:

    def __init__(self, text: str, org: Point):
        self._text = text
        self._org = org

    @property
    def text(self):
        return self._text

    @property
    def org(self):
        return self._org
