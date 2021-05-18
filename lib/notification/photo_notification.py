from lib.archive import Archive


class PhotoNotification:

    def __init__(self, archive: Archive, email: str):
        self.__archive = archive
        self.__email = email

    @property
    def archive(self):
        return self.__archive

    @property
    def email(self):
        return self.__email
