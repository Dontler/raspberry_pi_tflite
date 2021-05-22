import asyncio

from lib.http.client import HttpClient, ActionsEnum
from lib.notification.photo_notification import PhotoNotification


class Notifier:

    def __init__(self, client: HttpClient):
        self.__client = client

    def send_email_notification(self, notification: PhotoNotification):
        data = {'email': notification.email}
        photo_archive_file = notification.archive.flush()
        files = {'photo': None}
        with open(photo_archive_file, 'rb') as archive:
            files['photo'] = archive
            self.__client.post(action=ActionsEnum.MAIL_SEND_PHOTO, data=data, files=files)
