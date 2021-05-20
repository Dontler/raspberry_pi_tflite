import time

from lib.ai.object_detector import ObjectDetector, ObjectDetectorConfig
from lib.app_config import AppConfig
from lib.capture.video_capture import VideoCapture, VideoCaptureConfig
from lib.category import CategoryCollection, Category
from lib.http.client import HttpClient, ClientConfig
from lib.notification.notifier import Notifier
from lib.notification.notifier_facade import NotifierFacade
from lib.photo.photo_service import PhotoService, PhotoServiceConfig

LABELS_FILE = 'models/labelmap.txt'
MODEL_PATH = 'models/object_detection_model.tflite'
MODEL_WIDTH = 300
MODEL_HEIGHT = 300

if __name__ == '__main__':
    config = AppConfig.from_env()

    http_client_config = ClientConfig('http://localhost/')
    http_client = HttpClient(http_client_config)
    notifier = Notifier(http_client)
    notifier_facade = NotifierFacade(notifier)

    photo_service_config = PhotoServiceConfig('images/')
    photo_service = PhotoService(photo_service_config)

    categories = CategoryCollection.from_model(LABELS_FILE, config.accepted_classes)

    od_config = ObjectDetectorConfig(MODEL_PATH, MODEL_WIDTH, MODEL_HEIGHT)
    od = ObjectDetector(od_config)

    capture_config = VideoCaptureConfig(config.capture_source, MODEL_WIDTH, MODEL_HEIGHT, od.input_details.shape)

    vc = VideoCapture(capture_config)
    while True:
        img = vc.read_image()
        output = od.detect(img=img)
        for index, cls in enumerate(output.classes):
            if output.scores[index] < config.accepted_score:
                continue

            category = categories.get(index)
            if category is None or not category.is_accepted:
                continue
            box = output.boxes[index]
            h, w = img.source.shape[:2]
            if notifier_facade.is_dispatch_time(int(time.time())):
                archive = photo_service.build_archive()
                notifier_facade.send_photos(archive, config.default_email)
            else:
                photo_service.save_photo(img)

