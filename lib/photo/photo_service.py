import cv2
from time import time
import os

from lib.archive import Archive
from lib.capture.image import Image
from lib.notification.notifier_facade import NotifierFacade
from threading import Thread


class PhotoServiceConfig:

    def __init__(self, photo_folder: str, archives_folder: str):
        self.__photo_folder = photo_folder
        self.__archives_folder = archives_folder

    @property
    def photo_folder(self):
        return self.__photo_folder

    @property
    def archives_folder(self):
        return self.__archives_folder


class PhotoService:

    def __init__(self, config: PhotoServiceConfig, nf: NotifierFacade):
        self.__config = config
        self.__nf = nf

    def process_photo(self, photo: Image):
        if not self.__nf.is_dispatch_time(int(time())):
            self.save_photo(photo)
            return
        archive = self.build_archive()
        th = Thread(target=self.__nf.send_photos, args=[archive, 'ai@intervolga.ru'], daemon=True)
        th.start()
        self.clear_photos_folder()

    def save_photo(self, photo: Image):
        filename = '{0}/detection_{1}.jpg'.format(
            self.__config.photo_folder.rstrip('/'),
            str(int(time()))
        )
        cv2.imwrite(filename, photo.source)

    def build_archive(self) -> Archive:
        photos = os.listdir(self.__config.photo_folder)
        archive_name = '{0}/detections_{1}.zip'.format(
            self.__config.archives_folder.rstrip('/'),
            str(int(time()))
        )
        archive = Archive(archive_name)
        for photo in photos:
            photo_filename = '{0}/{1}'.format(
                self.__config.photo_folder.rstrip('/'),
                photo
            )
            archive.push(photo_filename)
        return archive

    def clear_photos_folder(self):
        photos = os.listdir(self.__config.photo_folder)
        for photo in photos:
            os.remove(photo)
