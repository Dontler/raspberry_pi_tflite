import time

from lib.archive import Archive
from lib.notification.notifier import Notifier
from lib.notification.photo_notification import PhotoNotification

HOUR_IN_SECONDS = 3600


class NotifierFacade:

    def __init__(self, notifier: Notifier):
        self.__notifier = notifier
        self.__last_notification_date = int(time.time())

    def send_photos(self, archive: Archive, email: str):
        current_time = int(time.time())
        if not self.is_dispatch_time(current_time):
            return

        notification = PhotoNotification(archive, email)
        self.__notifier.send_email_notification(notification)
        self.__last_notification_date = int(time.time())

    def is_dispatch_time(self, current_time: int):
        return current_time - self.__last_notification_date >= HOUR_IN_SECONDS
