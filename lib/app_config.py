import os


class AppConfig:

    def __init__(self, accepted_classes: list, accepted_score: int, capture_source: int, default_email: str):
        self.__accepted_classes = accepted_classes
        self.__accepted_score = accepted_score
        self.__capture_source = capture_source
        self.__default_email = default_email

    @property
    def accepted_classes(self):
        return self.__accepted_classes

    @property
    def accepted_score(self):
        return self.__accepted_score

    @property
    def capture_source(self):
        return self.__capture_source

    @property
    def default_email(self):
        return self.__default_email

    @staticmethod
    def from_env():
        ac = str(os.getenv('accepted_classes')).replace(' ', '').split(',')
        asc = int(os.getenv('accepted_score'))
        cs = int(os.getenv('capture_source'))
        de = os.getenv('default_email')

        return AppConfig(ac, asc, cs, de)
