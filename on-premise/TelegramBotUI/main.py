
import asyncio
import logging
from aiogram import Bot, Dispatcher
from decouple import config
from dotenv import load_dotenv
import os
from routers import text_router, callback_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения из .env файла
load_dotenv()

# Отладочная информация
print("Текущая директория:", os.getcwd())
print("Содержимое директории:", os.listdir())
print("BOT_TOKEN из .env:", os.getenv('BOT_TOKEN'))
print("BOT_TOKEN из config:", config('BOT_TOKEN'))

# Инициализация бота и диспетчера
bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(text_router)
dp.include_router(callback_router)

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
