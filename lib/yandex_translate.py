import requests


class YandexTranslateAPI:
    version = 2
    base_url = 'https://translate.api.cloud.yandex.net'

    def __init__(self, api_key, default_target_language=None):
        self.api_key = api_key
        self.default_target_language = default_target_language

    def translate(self, text, source_language=None, target_language=None):
        url = f'{self.base_url}/translate/v{self.version}/translate'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Authorization: Api-Key {self.api_key}',
        }

        body = {
            'texts': [text],
        }
        if target_language:
            body['targetLanguageCode'] = target_language.yandex_id
        elif self.default_target_language:
            body['targetLanguageCode'] = self.default_target_language.yandex_id
        if source_language:
            body['sourceLanguageCode'] = source_language.yandex_id

        response = requests.post(url, json=body, headers=headers)
        data = response.json()
        return data['translations'][0]['text']
