from lib.ai.object_detector import ObjectDetector, ObjectDetectorConfig
from lib.app_config import AppConfig
from lib.capture.image import Image
from lib.capture.video_capture import VideoCapture, VideoCaptureConfig
from lib.category import CategoryCollection
from lib.http.client import HttpClient, ClientConfig
from lib.notification.notifier import Notifier
from lib.notification.notifier_facade import NotifierFacade
from lib.photo.photo_service import PhotoService, PhotoServiceConfig

LABELS_FILE = 'models/labelmap.txt'
MODEL_PATH = 'models/object_detection_model.tflite'
MODEL_WIDTH = 300
MODEL_HEIGHT = 300


def main():
    config = AppConfig.from_env()

    http_client_config = ClientConfig('http://localhost/', '8000')
    http_client = HttpClient(http_client_config)
    notifier = Notifier(http_client)
    notifier_facade = NotifierFacade(notifier)

    photo_service_config = PhotoServiceConfig('detections/', 'archives/')
    photo_service = PhotoService(photo_service_config, notifier_facade)

    categories = CategoryCollection.from_model(LABELS_FILE, config.accepted_classes)

    od_config = ObjectDetectorConfig(MODEL_PATH, MODEL_WIDTH, MODEL_HEIGHT)
    od = ObjectDetector(od_config)

    capture_config = VideoCaptureConfig(config.capture_source, MODEL_WIDTH, MODEL_HEIGHT, od.input_details.shape)

    vc = VideoCapture(capture_config)
    while True:
        img = vc.read_image()
        output = od.detect(img=img)
        img_with_boxes = img
        has_matches = False
        for index, cls in enumerate(output.classes):
            if output.scores[index] < config.accepted_score:
                continue

            category = categories.get(index)
            if category is None or not category.is_accepted:
                continue
            has_matches = True
            box = output.boxes[index]
            h, w = img.source.shape[:2]
            img_with_boxes = Image.with_bounding_boxes(img_with_boxes, box, w, h,
                                                       category.name + ' ' + str(output.scores[index]))
        if has_matches:
            photo_service.process_photo(img_with_boxes)


if __name__ == '__main__':
    main()
