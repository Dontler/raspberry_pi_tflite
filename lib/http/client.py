import requests


class ClientConfig:

    def __init__(self, base_uri: str, port: str = '80'):
        self.__base_uri = base_uri
        self.__port = port

    @property
    def base_uri(self) -> str:
        return self.__base_uri

    @property
    def port(self) -> str:
        return self.__port


class HttpClient:

    def __init__(self, config: ClientConfig):
        self._config = config

    def post(self, action: str, data: dict, files: dict = None) -> dict:
        ActionsEnum.check_action(action)
        url = '{0}:{1}/{2}'.format(
            self._config.base_uri.rstrip('/'),
            self._config.port,
            action
        )

        response = requests.post(url, files=files, data=data)
        response_data = response.json()
        if type(response_data) is not dict:
            raise Exception('Invalid response type')

        return response_data


class ActionsEnum:
    MAIL_SEND_PHOTO = 'mail/send_photo'

    @staticmethod
    def check_action(action: str):
        if action is not ActionsEnum.MAIL_SEND_PHOTO:
            raise Exception('Invalid action')
