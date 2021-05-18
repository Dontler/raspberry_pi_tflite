from lib.http.client import HttpClient, ActionsEnum
from lib.notification.photo_notification import PhotoNotification


class Notifier:

    def __init__(self, client: HttpClient):
        self.__client = client

    def send_email_notification(self, notification: PhotoNotification):
        data = {'email': notification.email}
        files = {'photo': notification.archive.file}
        self.__client.post(action=ActionsEnum.MAIL_SEND_PHOTO, data=data, files=files)
