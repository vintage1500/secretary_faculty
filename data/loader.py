from telebot import TeleBot

from config import TOKEN
from database.database import MainManager, TableCreator

# Ensure tables exist (idempotent). This runs once at import time so the bot
# won't crash if tables are missing. If you prefer manual control, remove this.
creator = TableCreator()
creator.ensure_tables()

manager = MainManager()
bot = TeleBot(TOKEN)

