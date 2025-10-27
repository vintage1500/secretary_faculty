from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.loader import manager


def start_menu():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.row(
        InlineKeyboardButton(
            text="Часто задаваемые вопросы (FAQ)", callback_data="faq"
        ),
        InlineKeyboardButton(
            text="Как проходит обучение", callback_data="how_learning_goes"
        ),
    )
    markup.row(
        InlineKeyboardButton(text="Телефонный справочник", callback_data="telephone"),
        InlineKeyboardButton(text="Задать вопрос", callback_data="ask"),
    )
    markup.row(
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
        InlineKeyboardButton(text="Правила", callback_data="rules"),
    )
    return markup


def start_administrator_menu():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.row(InlineKeyboardButton(text="Ответить на вопрос", callback_data="answer"))
    markup.row(
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
        InlineKeyboardButton(text="Правила", callback_data="rules"),
    )
    return markup


def show_static_question_category():
    markup = InlineKeyboardMarkup(row_width=True)
    categories = manager.question_category.get_category()
    buttons = [
        InlineKeyboardButton(text=category[0], callback_data=f"category_{category[0]}")
        for category in categories
    ]
    markup.add(*buttons)
    markup.add(InlineKeyboardButton(text="Назад", callback_data="main"))
    return markup


def show_dynamic_question_category():
    markup = InlineKeyboardMarkup(row_width=True)
    categories = manager.question_category.get_category()
    buttons = [
        InlineKeyboardButton(text=category[0], callback_data=f"ctg_{category[0]}")
        for category in categories
    ]
    markup.add(*buttons)
    markup.add(InlineKeyboardButton(text="Назад", callback_data="main"))
    return markup


def show_category_answer():
    markup = InlineKeyboardMarkup(row_width=True)
    categories = manager.question_category.get_category()
    buttons = [
        InlineKeyboardButton(text=category[0], callback_data=f"acategory_{category[0]}")
        for category in categories
    ]
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Все категории", callback_data="allcateg"),
        InlineKeyboardButton(text="Назад", callback_data="main"),
    )
    return markup


def show_category_questions(category_name):
    markup = InlineKeyboardMarkup(row_width=True)
    questions = manager.dynamic_question.get_dynamic_question_by_category(category_name)
    for question in questions:
        text1 = " ".join(question[0:2])
        text1 += " " + question[3]
        # text1 += " " + question[6][:50]
        markup.add(InlineKeyboardButton(text=text1, callback_data="?"))
    markup.add(InlineKeyboardButton(text="Назад", callback_data="main"))
    return markup


def show_subcategories(category_id):
    markup = InlineKeyboardMarkup(row_width=True)
    subcategories = manager.question_subcategory.get_subcategories_by_category_id(
        category_id
    )
    buttons = [
        InlineKeyboardButton(
            text=subcategory[1], callback_data=f"subcat_{subcategory[0]}"
        )
        for subcategory in subcategories
    ]
    markup.add(*buttons)
    markup.add(InlineKeyboardButton(text="Назад", callback_data="faq"))
    return markup


def back_main():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(InlineKeyboardButton(text="Назад", callback_data="main"))
    return markup


def back_static_categories():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(InlineKeyboardButton(text="Назад", callback_data="faq"))
    return markup


def back_dynamic_categories():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(InlineKeyboardButton(text="Назад", callback_data="ask"))
    return markup


def how_to_learn_goes_markup():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Лекции", callback_data="how_learning_goes_lections"),
        InlineKeyboardButton(
            text="Семинарские занятия", callback_data="how_learning_goes_seminars"
        ),
        InlineKeyboardButton(text="ЛМС система", callback_data="how_learning_goes_lms"),
        InlineKeyboardButton(text="Назад", callback_data="how_learning_goes"),
        row_width=1,
    )
    return markup


def back_how_to_learn_goes():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(InlineKeyboardButton(text="Назад", callback_data="how_learning_goes"))
    return markup
