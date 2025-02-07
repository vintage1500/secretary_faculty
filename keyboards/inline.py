from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.loader import manager


def registration_menu():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.row(
        InlineKeyboardButton(text="Регистрация", callback_data=f"registration"),
    )
    return markup


def start_menu():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.row(
        InlineKeyboardButton(text="Часто задаваемые вопросы (FAQ)", callback_data=f"faq"),
    )
    markup.row(
        InlineKeyboardButton(text="Телефонный справочник", callback_data=f"telephone"),
        InlineKeyboardButton(text="Задать вопрос", callback_data=f"ask")
    )
    markup.row(
        InlineKeyboardButton(text="Профиль", callback_data=f"profile"),
        InlineKeyboardButton(text="Правила", callback_data=f"rules")
    )
    return markup


def start_administrator_menu():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.row(
        InlineKeyboardButton(text="Ответить на вопрос", callback_data=f"ask")
    )
    markup.row(
        InlineKeyboardButton(text="Профиль", callback_data=f"profile"),
        InlineKeyboardButton(text="Правила", callback_data=f"rules")
    )
    return markup


def show_static_question_category():
    markup = InlineKeyboardMarkup(row_width=True)
    categories = manager.static_question.get_static_question_category()
    buttons = [InlineKeyboardButton(text=category[0], callback_data=f"category_{category[0]}") for
               category in categories]
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"main")
    )
    return markup


def back_main():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"main")
    )
    return markup
