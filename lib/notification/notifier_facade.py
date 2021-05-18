from lib.archive import Archive
from lib.notification.notifier import Notifier
from lib.notification.photo_notification import PhotoNotification


class NotifierFacade:

    def __init__(self, notifier: Notifier):
        self.__notifier = notifier

    def send_photos(self, archive: Archive, email: str):
        notification = PhotoNotification(archive, email)
        self.__notifier.send_email_notification(notification)
