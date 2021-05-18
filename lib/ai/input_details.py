import numpy as np


class InputDetails:

    def __init__(self, shape: np.ndarray, index: int):
        self.__shape = shape
        self.__index = index

    @property
    def shape(self) -> np.ndarray:
        return self.__shape

    @property
    def index(self) -> int:
        return self.__index
