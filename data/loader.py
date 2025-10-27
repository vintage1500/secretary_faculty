# data/loader.py
import os
import telebot
from dotenv import load_dotenv
from data.api_client import APIClient

# Загружаем переменные окружения (.env)
load_dotenv()

# Получаем токен
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env")

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Создание REST-клиента
api = APIClient()
