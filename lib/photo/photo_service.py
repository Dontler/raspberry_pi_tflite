import cv2
import time
import os

from lib.archive import Archive
from lib.capture.image import Image


class PhotoServiceConfig:

    def __init__(self, photo_folder: str):
        self.__photo_folder = photo_folder

    @property
    def photo_folder(self):
        return self.__photo_folder


class PhotoService:

    def __init__(self, config: PhotoServiceConfig):
        self.__config = config

    def save_photo(self, photo: Image):
        filename = self.__config.photo_folder.rstrip('/') + 'detection_' + str(int(time.time()))
        cv2.imwrite(filename, photo.source)

    def build_archive(self) -> Archive:
        photos = os.listdir(self.__config.photo_folder)
        archive_name = 'detections_' + str(int(time.time()))
        archive = Archive(archive_name)
        for photo in photos:
            photo_filename = self.__config.photo_folder.rstrip('/') + photo
            archive.push(photo_filename)
        return archive

    def clear_folder(self):
        photos = os.listdir(self.__config.photo_folder)
        for photo in photos:
            os.remove(photo)
