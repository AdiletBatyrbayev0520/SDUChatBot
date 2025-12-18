from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from handlers import (
    start, process_language_callback, process_callback,
    info, stat, handle_text
)

# Создаем роутеры
text_router = Router()
callback_router = Router()

# Регистрируем обработчики для текстовых сообщений
text_router.message.register(start, Command("start"))
text_router.message.register(info, Command("info"))
text_router.message.register(stat, Command("stat"))
text_router.message.register(handle_text, F.text)

# Регистрируем обработчики для callback-запросов
callback_router.callback_query.register(process_language_callback, F.data.startswith('lang_'))
callback_router.callback_query.register(process_callback) 