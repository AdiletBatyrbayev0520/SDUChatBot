import sqlite3
from datetime import datetime, timedelta


class Database:
    def __init__(self, db_path='DataStore/database.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.update_table_structure()
        self.initialize_admins()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                             (user_id INTEGER PRIMARY KEY,
                              lang TEXT DEFAULT 'en');''')
        
        # Создаем таблицу администраторов
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS admins
                             (user_id INTEGER PRIMARY KEY,
                              added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
        self.conn.commit()

    def update_table_structure(self):
        # Проверяем наличие колонки registration_date в таблице users
        self.cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in self.cursor.fetchall()]
        
        if 'registration_date' not in columns:
            # Добавляем колонку registration_date
            self.cursor.execute('''ALTER TABLE users 
                                 ADD COLUMN registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;''')
            self.conn.commit()

    def initialize_admins(self):
        # Список администраторов по умолчанию
        default_admins = [741648725]  # Добавьте сюда нужные ID администраторов
        
        # Проверяем существующих администраторов
        self.cursor.execute("SELECT user_id FROM admins")
        existing_admins = [row[0] for row in self.cursor.fetchall()]
        
        # Добавляем новых администраторов
        for admin_id in default_admins:
            if admin_id not in existing_admins:
                self.cursor.execute('''INSERT INTO admins (user_id) VALUES (?);''', (admin_id,))
        
        self.conn.commit()

    def is_admin(self, user_id: int) -> bool:
        """Проверяет, является ли пользователь администратором"""
        return self.cursor.execute('''SELECT user_id FROM admins WHERE user_id = ?;''', (user_id,)).fetchone() is not None

    def add_admin(self, user_id: int) -> bool:
        """Добавляет нового администратора"""
        if not self.is_admin(user_id):
            self.cursor.execute('''INSERT INTO admins (user_id) VALUES (?);''', (user_id,))
            self.conn.commit()
            return True
        return False

    def remove_admin(self, user_id: int) -> bool:
        """Удаляет администратора"""
        if self.is_admin(user_id):
            self.cursor.execute('''DELETE FROM admins WHERE user_id = ?;''', (user_id,))
            self.conn.commit()
            return True
        return False

    def get_all_admins(self) -> list:
        """Возвращает список всех администраторов"""
        self.cursor.execute('''SELECT user_id FROM admins;''')
        return [row[0] for row in self.cursor.fetchall()]

    def exist_user(self, user_id: int) -> bool:
        return self.cursor.execute('''SELECT user_id FROM users WHERE user_id = ?;''', (user_id,)).fetchone() is not None

    def get_lang(self, user_id: int) -> str:
        result = self.cursor.execute('''SELECT lang FROM users WHERE user_id = ?;''', (user_id,)).fetchone()
        if result is None:
            # Если пользователь не найден, добавляем его с языком по умолчанию
            self.add_user(user_id)
            return 'en'
        return result[0]

    def add_user(self, user_id: int):
        if not self.exist_user(user_id):
            self.cursor.execute('''INSERT INTO users (user_id, registration_date) 
                                 VALUES (?, CURRENT_TIMESTAMP);''', (user_id,))
            self.conn.commit()

    def set_language(self, user_id: int, lang: str):
        self.cursor.execute('''UPDATE users SET lang = ? WHERE user_id = ?;''', (lang, user_id))
        self.conn.commit()

    def get_users_amount_hour(self) -> int:
        hour_ago = datetime.now() - timedelta(hours=1)
        return self.cursor.execute('''SELECT COUNT(*) FROM users WHERE registration_date >= ?;''', (hour_ago,)).fetchone()[0]

    def get_users_amount_day(self) -> int:
        day_ago = datetime.now() - timedelta(days=1)
        return self.cursor.execute('''SELECT COUNT(*) FROM users WHERE registration_date >= ?;''', (day_ago,)).fetchone()[0]

    def get_users_amount_whole(self) -> int:
        return self.cursor.execute('''SELECT COUNT(*) FROM users;''').fetchone()[0]


if __name__ == '__main__':
    db = Database()
