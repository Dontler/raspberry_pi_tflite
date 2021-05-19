import cv2
import numpy as np


class Image:

    def __init__(self, source: np.ndarray):
        self.__source = source

    @property
    def source(self) -> np.ndarray:
        return self.__source

    @staticmethod
    def default(shape: np.ndarray):
        return Image(np.ndarray(shape=shape))

    @staticmethod
    def to_rgb(img, width: int, height: int):
        img_rgb = cv2.cvtColor(img.source, cv2.COLOR_BGR2RGB)
        return Image(cv2.resize(img_rgb, (height, width), cv2.INTER_NEAREST))
