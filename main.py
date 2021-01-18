import cv2
import sys
import argparse
import config


from lib.notifier import send_image
from lib.object_detection import prepare_interpreter, prepare_output_data
from lib.visualization import draw_matched_area, prepare_rgb_image


accepted_classes = config.ACCEPTED_CLASSES
accepted_score = config.ACCEPTED_SCORE
capture_source = config.CAPTURE_SOURCE
email = config.DEFAULT_EMAIL


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--classes')
    parser.add_argument('-s', '--score')
    parser.add_argument('-S', '--source')
    parser.add_argument('-e', '--email')

    return parser


def prepare_accepted_classes(input_data: str) -> list:
    return input_data.replace(' ', '').split(',')


def create_indexes(label_path='models/labelmap.txt', classes=None) -> dict:
    category_indexes = {}
    with open(label_path) as labels:
        for i, val in enumerate(labels):
            if i != 0:
                label = val[:-1]
                if label != '???':
                    if classes is None or len(classes) < 1:
                        category_indexes.update({(i-1): {'id': (i-1), 'name': label}})
                        continue
                    if label not in classes:
                        continue
                    category_indexes.update({(i - 1): {'id': (i - 1), 'name': label}})

    return category_indexes


if __name__ == '__main__':
    namespace = build_argparser().parse_args(sys.argv[1:])
    if namespace.classes is not None:
        accepted_classes = prepare_accepted_classes(namespace.classes)
    if namespace.score is not None:
        accepted_score = float(namespace.score)
    if namespace.source is not None:
        capture_source = namespace.source
        if capture_source.isdigit():
            capture_source = int(capture_source)
    if namespace.email is not None:
        email = namespace.email

    categories = create_indexes(classes=accepted_classes)

    capture = cv2.VideoCapture(capture_source)
    if not capture.isOpened():
        exit(404)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

    interpreter = prepare_interpreter('models/object_detection_model.tflite')
    input_details = interpreter.get_input_details()
    input_shape = input_details[0]['shape']
    index = input_details[0]['index']

    while True:
        ret, img = capture.read()
        if img is not None:
            img_rgb = prepare_rgb_image(img, 300, 300, input_shape)

            interpreter.set_tensor(input_details[0]['index'], img_rgb)
            interpreter.invoke()

            output_details = interpreter.get_output_details()
            output = prepare_output_data(interpreter, output_details)

            temp_img = img
            for id, cls in enumerate(output['classes']):
                if cls not in categories or output['scores'][id] <= accepted_score:
                    continue
                box = output['boxes'][id]
                h, w = temp_img.shape[:2]
                temp_img = draw_matched_area(temp_img, box, w, h, categories[cls]['name'])
                # cv2.imwrite('images/detection.jpg', temp_img)
                # send_image('\\images\\detection.jpg', email)

            cv2.imshow('capture', temp_img)
            key = cv2.waitKey(1)
            if key == 27:
                break

    capture.release()
    cv2.destroyAllWindows()
