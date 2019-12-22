from urllib.parse import urlencode
from typing import Dict
import requests

from ycloud import auth


class Component:
    MAIN_PART_URL = 'api.cloud.yandex.net'
    COMPONENT_NAME = ''

    CONNECT_TIMEOUT = 10
    READ_TIMEOUT = 60

    def __init__(self, auth: auth):
        self.auth = auth

    def _request(self, method, path, data, options=None, version=1):

        options = options or {}

        url = self._compose_url(version, path, options)

        token = self.auth.get_iam_token()
        headers = {
            'Authorization': 'Bearer ' + token['iamToken']
        }

        try:
            if method == 'POST':
                r = requests.post(url, headers=headers, json=data, timeout=(self.CONNECT_TIMEOUT, self.READ_TIMEOUT))
            else:
                r = requests.get(url, headers=headers, timeout=(self.CONNECT_TIMEOUT, self.READ_TIMEOUT))

            if r.status_code == requests.codes.ok:
                return r.text
            else:
                return None
        except requests.exceptions.RequestException as e:
            return None

    def _compose_url(self, version: str, path: str, options: Dict):
        result = f'https://{self.COMPONENT_NAME}.{self.MAIN_PART_URL}/{self.COMPONENT_NAME}/v{version}/{path}'
        if options:
            result = f'{result}?{urlencode(options)}'
        return result


class Vision(Component):
    COMPONENT_NAME = 'vision'

    def batchAnalyze(self, data):
        return self._request('POST', 'batchAnalyze', data)
