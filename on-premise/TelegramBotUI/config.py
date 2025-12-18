import os

# Базовые пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, 'input_files')

# Пути к файлам меню
AUTH_FILE = os.path.join(INPUT_DIR, 'authorization', 'authorization.json')
MAIN_MENU_DIR = os.path.join(INPUT_DIR, 'main_menu')
BACK_BUTTON_FILE = os.path.join(INPUT_DIR, 'back_button.json')

# Пути к изображениям
IMAGES_DIR = os.path.join(BASE_DIR, 'images') 