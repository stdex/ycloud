# encoding: utf-8
import base64
import json
import os
import unittest
import ycloud

OAUTH_TOKEN = ''


class ApiTest(unittest.TestCase):

    def testAuth(self):
        auth = ycloud.SimpleAuth(OAUTH_TOKEN)
        assert auth.oauth_token == OAUTH_TOKEN

    def testIAMAuth(self):
        auth = ycloud.SimpleAuth(OAUTH_TOKEN)
        token = auth.get_iam_token()
        assert len(token['iamToken']) != 0

    def testVisionImageModeration(self):
        auth = ycloud.SimpleAuth(OAUTH_TOKEN)
        api = ycloud.API(auth)

        dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(dir, '1.jpg')

        outfile = self._encode_file(filepath)

        data = {
            "folderId": "",
            "analyze_specs": [
                {
                    "content": outfile,
                    "features": [
                        {
                            "type": "CLASSIFICATION",
                            "classificationConfig": {
                                "model": "moderation"
                            }
                        }
                    ]
                }
            ]
        }

        response = api.vision.batchAnalyze(data)
        result = json.loads(response)
        assert ('results' in result)

    def _encode_file(self, file):
        with open(file, 'rb') as f:
            file_content = f.read()
        return base64.b64encode(file_content).decode('utf-8')
