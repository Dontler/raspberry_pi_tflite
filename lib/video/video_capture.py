import cv2


class VideoCapture:

    def __init__(self, source: str):
        capture = cv2.VideoCapture(source)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

        self.__capture = capture

    def read_image_rgb(self):
        if not self.__capture.isOpened():
            raise Exception('Source is not specified or unavailable')

        ret, img = self.__capture.read()
        if img is None:
            return None

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BRGB)
        img_rgb = cv2.resize(img_rgb, (300, 300), cv2.INTER_NEAREST)
        return img_rgb.reshape(shape=shape)
