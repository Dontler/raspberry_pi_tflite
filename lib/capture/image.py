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

    @staticmethod
    def with_bounding_boxes(img, box, width: int, height: int, label: str = None):
        p1 = (int(box[1] * width), int(box[0] * height))
        p2 = (int(box[3] * width), int(box[2] * height))

        out_img = img.source
        if label is not None:
            org = (p1[0], p1[1] + 20)
            out_img = cv2.putText(out_img, label, org, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return Image(cv2.rectangle(out_img, p1, p2, color=(0, 255, 0)))
