# Імпортуємо необхідні модулі
import os
from dotenv import load_dotenv

# Завантажуємо змінні з .env файлу
load_dotenv()

# Отримуємо токени з .env файлу
CHATGPT_TOKEN = os.getenv("CHATGPT_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Виводимо токени в консоль (Видалити після перевірки)
print(CHATGPT_TOKEN)
print(BOT_TOKEN)