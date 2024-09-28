from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import manager


def start_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton(text="Часто задаваемые вопросы"),
        KeyboardButton(text="Задать вопрос")
    )
    return markup


def start_administrator_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton(text="Часто задаваемые вопросы"),
        KeyboardButton(text="Принять запрос")
        )
    return markup
