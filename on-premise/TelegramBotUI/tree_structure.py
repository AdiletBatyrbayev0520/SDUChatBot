from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import Database as db
import json
import os

@dataclass
class Content:
    """Класс для хранения контента узла"""
    text: str
    button_text: str  # Текст для кнопки
    img: Optional[List[str]] = None  # Пыути к изображениям
    url: Optional[str] = None  # URL для кнопки-ссылки

class Node:
    """Класс для представления узла в дереве"""
    def __init__(self, 
                 key: int,
                 content: Content,
                 callback_data: str,
                 prev: Optional['Node'] = None,
                 children: List['Node'] = None):
        self.key = key
        self.content = content
        self.callback_data = callback_data
        self.prev = prev
        self.children = children or []

    @classmethod
    def from_dict(cls, data: Dict[str, Any], prev: Optional['Node'] = None, key_counter: int = 0) -> 'Node':
        """Создание узла из словаря"""
        content = Content(
            text=data['text'],
            button_text=data.get('button_text', data['text']),  # Используем text как fallback
            img=data.get('img'),
            url=data.get('url')
        )

        # Для узлов с URL используем специальный callback_data
        callback_data = data.get('callback_data')
        if not callback_data and data.get('url'):
            callback_data = f"url_{key_counter}"

        node = cls(
            key=key_counter,
            content=content,
            callback_data=callback_data,
            prev=prev
        )

        children = []
        if 'children' in data:
            # Если children - список
            if isinstance(data['children'], list):
                for child_data in data['children']:
                    key_counter += 1
                    child = cls.from_dict(child_data, prev=node, key_counter=key_counter)
                    children.append(child)
            # Если children - одиночный словарь
            elif isinstance(data['children'], dict):
                key_counter += 1
                child = cls.from_dict(data['children'], prev=node, key_counter=key_counter)
                children.append(child)

        node.children = children
        return node

    def add_child(self, child):
        self.children.append(child)
        child.prev = self

class ButtonTree:
    """Класс для работы с деревом кнопок"""
    def __init__(self, root: Node):
        self.root = root
        self.nodes = {}
        self._build_node_dict(root)
        # Загружаем тексты кнопки "Назад"
        with open('input_files/back_button.json', 'r', encoding='utf-8') as f:
            self.back_button_texts = json.load(f)

    def _build_node_dict(self, node: Node):
        """Строит карту callback -> node и массив ключей"""
        self.nodes[node.callback_data] = node
        for child in node.children:
            self._build_node_dict(child)

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'ButtonTree':
        """Создание дерева из JSON данных"""
        root = Node.from_dict(json_data)
        return cls(root)

    def get_node(self, callback_data: str) -> Optional[Node]:
        """Получить узел по callback_data"""
        return self.nodes.get(callback_data)

    def create_keyboard(self, node: Node, user_id: int = None, lang: str = 'en') -> InlineKeyboardMarkup:
        """Создает клавиатуру для узла"""
        builder = InlineKeyboardBuilder()
        
        # Добавляем кнопки для дочерних узлов
        for child in node.children:
            callback_data = child.callback_data
            builder.button(text=child.content.button_text, callback_data=callback_data)
        
        # Добавляем кнопку "Назад" если есть родительский узел
        if node.prev:
            back_text = self.back_button_texts.get(lang, self.back_button_texts['en'])
            builder.button(text=back_text, callback_data=node.prev.callback_data)
        
        # Добавляем кнопку "Главное меню" если это не корневой узел
        if node != self.root:
            main_menu_text = self.back_button_texts.get('main_menu', {}).get(lang, self.back_button_texts['main_menu']['en'])
            builder.button(text=main_menu_text, callback_data="main_menu")
        
        builder.adjust(2)
        return builder.as_markup()