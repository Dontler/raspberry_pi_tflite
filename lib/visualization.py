import cv2

from lib.geometry.point import Point
from lib.geometry.rectangle import Rectangle
from lib.label import Label


def resize_image(img, width: int, height: int):
    return cv2.resize(img, (width, height), cv2.INTER_NEAREST)


def draw_matched_area(img, box, width, height, label: str = None):
    p1 = Point(box[1] * width, box[0] * height)
    p2 = Point(box[3] * width, box[2] * height)
    rectangle = Rectangle(p1, p2)

    if label is not None:
        label = Label(label, p1)
        org = (label.org.x, label.org.y + 20)
        img = cv2.putText(img, label.text, org, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return cv2.rectangle(img, rectangle.p1.to_tuple(), rectangle.p2.to_tuple(), color=(0, 255, 0))


def prepare_rgb_image(img, width, height, shape):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = resize_image(img_rgb, width, height)
    return img_rgb.reshape(shape)