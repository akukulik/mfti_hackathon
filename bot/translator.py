import requests # для выполнения HTTP-запросов к API
import logging # для логирования ошибок и событий

from dataclasses import dataclass # для создания классов данных
from functools import lru_cache # для кэширования вызовов функций

# Настройка логгера для вывода информации об ошибках
logger = logging.getLogger(__name__)


# Класс для представления результата перевода текста
@dataclass
class TranslationResult:
    translated_text: str  # переведенный текст
    detected_language: str  # исходный язык текста, определенный API
    success: bool  # флаг успешного выполнения перевода


# Класс для работы с Yandex Translation API
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
        """
        Выполняет перевод текста с указанного языка на целевой язык.

        :param text: Текст для перевода
        :param target_language: Целевой язык (по умолчанию 'en')
        :param source_language: Исходный язык (по умолчанию 'ru')
        :return: Объект TranslationResult с результатами перевода
        """
        try:
            # Формируем тело запроса
            payload = {
                'folder_id': self.folder_id,
                'texts': [text],
                'targetLanguageCode': target_language,
                'sourceLanguageCode': source_language,
            }

            # Отправляем POST-запрос на URL для перевода текста
            response = requests.post(
                f'{self.BASE_URL}/translate',
                headers=self.headers,
                json=payload
            )

            # Проверяем успешность ответа (код 2xx)
            response.raise_for_status()

            # Парсим JSON-ответ
            data = response.json()

            # Если переводы отсутствуют в ответе, выбрасываем исключение
            if not data.get('translations'):
                raise ValueError('Переводы не были получены при переводе из API')

            translation = data['translations'][0]

            # Возвращаем успешный результат перевода
            return TranslationResult(
                translated_text=translation['text'],
                detected_language=translation.get('detectedLanguageCode', 'unknown'),
                success=True
            )

        except Exception as e:
            # Логируем ошибку и возвращаем результат с флагом неудачи
            logger.error(f'Ошибка при переводе: {str(e)}')
            return TranslationResult(
                translated_text='',
                detected_language='',
                success=False
            )

    def detect_language(self, text: str) -> str | None:
        """
        Определяет язык текста с помощью Yandex Translation API.

        :param text: Текст для анализа
        :return: Код языка или None в случае ошибки
        """
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


# Функция для кэшированного создания экземпляра YandexTranslationService
@lru_cache
def get_translator_service(api_key: str, folder_id: str) -> YandexTranslationService:
    """Возращает сервис-переводчик для переводов текстов."""
    return YandexTranslationService(
        api_key=api_key,
        folder_id=folder_id,
    )
