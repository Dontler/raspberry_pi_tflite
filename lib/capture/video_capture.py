import cv2

from lib.capture.image import Image


class VideoCaptureConfig:

    def __init__(self, source: str, width: int, height: int, shape):
        self.__source = source
        self.__width = width
        self.__height = height
        self.__shape = shape

    @property
    def source(self):
        return self.__source

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def shape(self):
        return self.__shape


class VideoCapture:

    def __init__(self, config: VideoCaptureConfig):
        self.__config = config

        capture = cv2.VideoCapture(config.source)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

        self.__capture = capture

    def read_image(self) -> Image:
        if not self.__capture.isOpened():
            raise Exception('Source is not specified or unavailable')

        ret, img = self.__capture.read()
        if img is None:
            return Image.default(self.__config.shape)

        return Image(img)
