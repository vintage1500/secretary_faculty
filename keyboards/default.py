from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import manager


def reg_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton(text="Регистрация")
    )
    return markup
