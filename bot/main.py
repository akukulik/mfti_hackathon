import os
import asyncio
import httpx

from typing import Any

from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from translator import YandexTranslationService, get_translator_service

load_dotenv()


class Config:
    # Yandex Translator
    YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
    YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')
    # Telegram
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    MODEL_SERVICE_URL = 'http://model:8000/predict'


translator_service: YandexTranslationService = get_translator_service(Config.YANDEX_API_KEY, Config.YANDEX_FOLDER_ID)

bot = Bot(token=Config.BOT_TOKEN)

dp = Dispatcher()


def format_model_results(result: list[dict[str, Any]]) -> str:
    """Форматирует результаты из нейронной модели."""

    label: str = result[0]['label']
    score: str = result[0]['score']

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


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply(
        'Привет! Отправь мне текст, и я обработаю его с помощью нейронной модели.\n'
        'Результатом работы будет предполагаемая оценка наличия депрессии (отсутствует, умеренная, сильная).\n'
        'Важно! Этот бот не ставит диагноз, если вы заподозрили у себя любые симптомы - необходимо обратиться ко врачу!'
    )


@dp.message()
async def process_message(message: types.Message):
    user_text = message.text

    translated_text = translator_service.translate_text(user_text).translated_text

    async with httpx.AsyncClient() as client:
        response = await client.post(Config.MODEL_SERVICE_URL, json={'text': translated_text})

    if response.status_code == 200:
        result = format_model_results(response.json()['result'])

        await message.reply(f'Результат обработки:\n\n{result}')
    else:
        await message.reply('Произошла ошибка при обработке запроса.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
