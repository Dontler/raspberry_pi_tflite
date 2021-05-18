import numpy as np


class OutputDetails:

    def __init__(self, boxes: np.ndarray, classes: np.ndarray, scores: np.ndarray, num: int):
        self.__boxes = boxes
        self.__classes = classes
        self.__scores = scores
        self.__num = num

    @property
    def boxes(self) -> np.ndarray:
        return self.__boxes

    @property
    def classes(self) -> np.ndarray:
        return self.__classes

    @property
    def scores(self) -> np.ndarray:
        return self.__scores

    @property
    def num(self) -> int:
        return self.__num
