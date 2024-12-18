import requests
import logging

from dataclasses import dataclass
from functools import lru_cache


logger = logging.getLogger(__name__)


@dataclass
class TranslationResult:
    translated_text: str
    detected_language: str
    success: bool


class YandexTranslationService:
    BASE_URL = 'https://translate.api.cloud.yandex.net/translate/v2'

    def __init__(self, api_key: str, folder_id: str):
        self.api_key = api_key
        self.folder_id = folder_id
        self.headers = {
            'Authorization': f'Api-Key {api_key}',
            'Content-Type': 'application/json'
        }

    def translate_text(
            self,
            text: str,
            target_language: str = 'en',
            source_language: str = 'ru',
    ) -> TranslationResult:
        try:
            payload = {
                'folder_id': self.folder_id,
                'texts': [text],
                'targetLanguageCode': target_language,
                'sourceLanguageCode': source_language,
            }

            response = requests.post(
                f'{self.BASE_URL}/translate',
                headers=self.headers,
                json=payload
            )

            response.raise_for_status()
            data = response.json()

            if not data.get('translations'):
                raise ValueError('Переводы не были получены при переводе из API')

            translation = data['translations'][0]

            return TranslationResult(
                translated_text=translation['text'],
                detected_language=translation.get('detectedLanguageCode', 'unknown'),
                success=True
            )

        except Exception as e:
            logger.error(f'Ошибка при переводе: {str(e)}')
            return TranslationResult(
                translated_text='',
                detected_language='',
                success=False
            )

    def detect_language(self, text: str) -> str | None:
        try:
            payload = {
                'folder_id': self.folder_id,
                'text': text
            }

            response = requests.post(
                f'{self.BASE_URL}/detect',
                headers=self.headers,
                json=payload
            )

            response.raise_for_status()
            data = response.json()

            return data.get('languageCode')

        except Exception as e:
            logger.error(f'Ошибка при распознавании языка: {str(e)}')


@lru_cache
def get_translator_service(api_key: str, folder_id: str) -> YandexTranslationService:
    """Возращает сервис-переводчик для переводов текстов."""
    return YandexTranslationService(
        api_key=api_key,
        folder_id=folder_id,
    )
