import requests


class ClientConfig:

    def __init__(self, base_uri: str):
        self.__base_uri = base_uri

    @property
    def base_uri(self) -> str:
        return self.__base_uri


class HttpClient:

    def __init__(self, config: ClientConfig):
        self._config = config

    def post(self, action: str, data: dict, files: dict = None) -> dict:
        ActionsEnum.check_action(action)
        url = self._config.base_uri.rstrip('/') + action

        response = requests.post(url, files=files, data=data)
        response_data = response.json()
        if response is not dict:
            raise Exception('Invalid response type')

        return response_data


class ActionsEnum:
    MAIL_SEND_PHOTO = '/mail/send_photo'

    @staticmethod
    def check_action(action: str):
        if str is not ActionsEnum.MAIL_SEND_PHOTO:
            raise Exception('Invalid action')
