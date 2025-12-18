from aiogram import types
from aiogram.types import InputMediaPhoto, Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from db import Database
from tree_structure import ButtonTree
from config import MAIN_MENU_DIR, AUTH_FILE, BACK_BUTTON_FILE
import json
import os
import aiohttp
from decouple import config
from loguru import logger
db = Database()


ENDPOINTS = [
    "http://llm_agent-backend:8001/ask",
    "http://localhost:8001/ask"
]



with open(AUTH_FILE, 'r', encoding='utf-8') as f:
    auth_config = json.load(f)
auth_tree = ButtonTree.from_json(auth_config)


menu_trees = {}
menu_dir = MAIN_MENU_DIR
dir_name = os.path.basename(menu_dir)  
for filename in os.listdir(menu_dir):
    if filename.endswith('.json'):
        lang = filename.replace(f'{dir_name}_', '').replace('.json', '')  
        with open(os.path.join(menu_dir, filename), 'r', encoding='utf-8') as f:
            menu_config = json.load(f)
            menu_trees[lang] = ButtonTree.from_json(menu_config)


with open(BACK_BUTTON_FILE, 'r', encoding='utf-8') as f:
    back_button_texts = json.load(f)

async def start(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    
    if db.exist_user(user_id) and db.get_lang(user_id):
        lang = db.get_lang(user_id)
        menu_tree = menu_trees[lang]
        
        await message.answer(
            menu_tree.root.content.text,
            reply_markup=menu_tree.create_keyboard(menu_tree.root, user_id, lang),
            parse_mode='Markdown'
        )
    else:
        
        await message.answer(
            auth_tree.root.content.text,
            reply_markup=auth_tree.create_keyboard(auth_tree.root, user_id, 'en'),
            parse_mode='Markdown'
        )

async def process_language_callback(callback_query: CallbackQuery):
    """Обработчик выбора языка"""
    user_id = callback_query.from_user.id
    lang = callback_query.data.split('_')[1]  
    
    
    if not db.exist_user(user_id):
        db.add_user(user_id)
    db.set_language(user_id, lang)
    
    
    menu_tree = menu_trees[lang]
    await callback_query.message.edit_text(
        menu_tree.root.content.text,
        reply_markup=menu_tree.create_keyboard(menu_tree.root, user_id, lang),
        parse_mode='Markdown'
    )
    await callback_query.answer()

async def process_callback(callback_query: CallbackQuery):
    """Обработчик всех остальных callback-запросов"""
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    
    
    lang = db.get_lang(user_id)
    current_tree = menu_trees[lang] if lang else auth_tree
    
    
    node = current_tree.get_node(callback_data)
    if not node:
        await callback_query.answer("❌ Ошибка: кнопка не найдена")
        return

    
    if node.content.img:
        
        media = []
        for i, img_path in enumerate(node.content.img):
            
            if i == 0:
                media.append(InputMediaPhoto(
                    media=FSInputFile(img_path),
                    caption=node.content.text,
                    parse_mode='Markdown'
                ))
            else:
                media.append(InputMediaPhoto(
                    media=FSInputFile(img_path)
                ))
        
        
        await callback_query.message.answer_media_group(media=media)
        
        
        await callback_query.message.answer(
            node.content.text,
            reply_markup=current_tree.create_keyboard(node, user_id, lang),
            parse_mode='Markdown'
        )
        
        
        await callback_query.message.delete()
    else:
        
        await callback_query.message.edit_text(
            node.content.text,
            reply_markup=current_tree.create_keyboard(node, user_id, lang),
            parse_mode='Markdown'
        )
    
    await callback_query.answer()

async def info(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    if not lang:
        await message.answer("❌ Please select language first using /start")
        return
        
    menu_tree = menu_trees[lang]
    info_node = menu_tree.get_node("info_menu")
    if info_node:
        await message.answer(
            info_node.content.text, 
            reply_markup=menu_tree.create_keyboard(info_node, user_id, lang),
            parse_mode='Markdown'
        )

async def stat(message: Message):
    user_id = message.from_user.id
    if not db.is_admin(user_id):
        return
    hour = db.get_users_amount_hour()
    day = db.get_users_amount_day()
    whole = db.get_users_amount_whole()
    stats_text = "📊 *Статистика регистраций*\n\n"
    stats_text += f"За последний час: {hour}\n"
    stats_text += f"За последние 24 часа: {day}\n"
    stats_text += f"Всего: {whole}"
    await message.answer(
        stats_text,
        parse_mode='Markdown'
    )

async def handle_text(message: Message):
    """Обработчик текстовых сообщений"""
    
    processing_msg = await message.answer("🔄 Сообщение обрабатывается...")
    
    language = db.get_lang(message.from_user.id)
    last_error = None
    
    async with aiohttp.ClientSession() as session:
        for endpoint in ENDPOINTS:
            try:
                async with session.post(
                    endpoint,
                    json={"user_id": message.from_user.id, "question": message.text, "language": language},
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        answer = data["answer"]
                        tokens = data["tokens"]
                        cost = data["cost"]
                        source_documents_dict = data["source_documents_dict"]
                        
                        response_text = f"{answer}\n\n"
                        for source, relevance_score in source_documents_dict.items():
                            response_text += f"🔍 Источник: {os.path.basename(source)}\n"
                        
                        
                        await processing_msg.delete()
                        await message.answer(response_text)
                        logger.info(f"Ответ от {endpoint}: {response_text}")
                        return
                    else:
                        error_text = await response.text()
                        last_error = f"❌ Ошибка при обработке запроса: {error_text}"
            except Exception as e:
                last_error = f"❌ Ошибка при подключении к {endpoint}: {str(e)}"
                continue
    
    
    await processing_msg.edit_text(last_error) 