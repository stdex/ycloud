import json
import requests
import os
import time
from datetime import datetime, timedelta
import tempfile

IAM_TOKENS_BASE_URL = 'https://iam.api.cloud.yandex.net'
IAM_TOKENS_URL = IAM_TOKENS_BASE_URL + '/iam/v1/tokens'

IAM_TOKEN_MAX_AGE = 11 * 60 * 60
IAM_TOKEN_PATH = os.path.join(
    tempfile.gettempdir(),
    'ycloud',
    'iam.token',
)

IAM_TOKEN_EXPIRES_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
IAM_TOKEN_EXPIRES_MINUTES_DELTA = 10


class SimpleAuth(object):
    def __init__(self, oauth_token):
        self.oauth_token = oauth_token

    def request_iam_token(self):

        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'yandexPassportOauthToken': self.oauth_token
        }
        r = requests.post(IAM_TOKENS_URL, data=json.dumps(data), headers=headers)
        data = r.text

        if not data:
            return None

        token = json.loads(data)

        if not self.is_iam_token_correct(token):
            return None

        dirname = os.path.dirname(IAM_TOKEN_PATH)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(IAM_TOKEN_PATH, 'w') as outfile:
            outfile.write(data)

        return token

    def is_iam_token_correct(self, token):
        if (token is not None) and ('iamToken' in token) and ('expiresAt' in token):
            return True
        return False

    def is_iam_token_expires(self, token):
        expiresAt = datetime.strptime(token['expiresAt'], IAM_TOKEN_EXPIRES_DATETIME_FORMAT)
        if expiresAt - timedelta(minutes=IAM_TOKEN_EXPIRES_MINUTES_DELTA) <= datetime.now():
            return True
        return False

    def get_iam_token(self, force=False):

        if force:
            return self.request_iam_token()

        token = None

        if os.path.isfile(IAM_TOKEN_PATH):
            token_age = time.time() - os.path.getmtime(IAM_TOKEN_PATH)

            if token_age < IAM_TOKEN_MAX_AGE:
                with open(IAM_TOKEN_PATH, 'r') as infile:
                    data = infile.read()
                    token = json.loads(data)
                    if self.is_iam_token_expires(token):
                        token = self.request_iam_token()
            else:
                token = self.request_iam_token()
        else:
            token = self.request_iam_token()

        return token
