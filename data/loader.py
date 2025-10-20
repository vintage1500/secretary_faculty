from telebot import TeleBot

from config import TOKEN
from database.database import MainManager, TableCreator

# Initialize DB schema safely before using the bot
_creator = TableCreator()
_creator.create_all_tables()

manager = MainManager()
# Initialize basic categories
manager.data_initializer.initialize_basic_categories()

bot = TeleBot(TOKEN)

