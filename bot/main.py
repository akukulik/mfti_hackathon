import os
import asyncio # для работы с асинхронным кодом
import httpx # для выполнения асинхронных HTTP-запросов

from typing import Any # для аннотаций типов

from aiogram.filters import Command # фильтр для обработки команд Telegram
from dotenv import load_dotenv # для загрузки переменных окружения из .env файла
from aiogram import Bot, Dispatcher, types # основные классы для работы с Telegram API

from translator import YandexTranslationService, get_translator_service

# Загрузка переменных окружения из .env файла
load_dotenv()


# Класс конфигурации для хранения настроек приложения
class Config:
    # Yandex Translator
    YANDEX_API_KEY = os.getenv('YANDEX_API_KEY') # API-ключ для Яндекс Переводчика
    YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID') # ID папки в Яндекс Облаке
    # Telegram
    BOT_TOKEN = os.getenv('BOT_TOKEN')  # Токен Telegram-бота
    MODEL_SERVICE_URL = 'http://model:8000/predict'   # URL сервиса для обработки текстов нейромоделью

# Инициализация сервиса перевода с использованием API-ключа и ID папки
translator_service: YandexTranslationService = get_translator_service(Config.YANDEX_API_KEY, Config.YANDEX_FOLDER_ID)

# Создание экземпляра Telegram-бота
bot = Bot(token=Config.BOT_TOKEN)

# Создание диспетчера для обработки событий
dp = Dispatcher()


# Функция для форматирования результатов работы нейросети
def format_model_results(result: list[dict[str, Any]]) -> str:
    """Форматирует результаты из нейронной модели."""

    label: str = result[0]['label'] # Получаем метку классификации
    score: str = result[0]['score'] # Получаем уверенность модели

    # Определяем текстовое описание по метке
    match label:
        case 'not depression':
            text = 'Депрессия отсутствует или мало выражена'
        case 'moderate':
            text = 'Умеренная депрессия'
        case 'severe':
            text = 'Сильная депрессия'
        case _:
            raise Exception('Что-то пошло не так')

    text += f'\nУверенность модели: {int(score * 100)}%'
    return text


# Обработчик команд /start и /help
@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply(
        'Привет! Отправь мне текст, и я обработаю его с помощью нейронной модели.\n'
        'Результатом работы будет предполагаемая оценка наличия депрессии (отсутствует, умеренная, сильная).\n'
        'Важно! Этот бот не ставит диагноз, если вы заподозрили у себя любые симптомы - необходимо обратиться ко врачу!'
    )


# Обработчик всех других текстовых сообщений
@dp.message()
async def process_message(message: types.Message):
    user_text = message.text # Получаем текст сообщения пользователя

    # Перевод текста с помощью сервиса Yandex Translation
    translated_text = translator_service.translate_text(user_text).translated_text

    # Отправка переведенного текста в сервис модели
    async with httpx.AsyncClient() as client:
        response = await client.post(Config.MODEL_SERVICE_URL, json={'text': translated_text})

    # Если модель успешно обработала запрос, отправляем результат пользователю
    if response.status_code == 200:
        result = format_model_results(response.json()['result'])

        await message.reply(f'Результат обработки:\n\n{result}')
    else:
        # В случае ошибки обработки отправляем уведомление
        await message.reply('Произошла ошибка при обработке запроса.')


# Асинхронная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
