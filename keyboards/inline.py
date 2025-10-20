from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.loader import manager


def start_menu():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.row(
        InlineKeyboardButton(text="Часто задаваемые вопросы (FAQ)", callback_data=f"faq"),
    )
    markup.row(
        InlineKeyboardButton(text="Как добраться до...", callback_data=f"way"),
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
        InlineKeyboardButton(text="Ответить на вопрос", callback_data=f"answer")
    )
    markup.row(
        InlineKeyboardButton(text="Профиль", callback_data=f"profile"),
        InlineKeyboardButton(text="Правила", callback_data=f"rules")
    )
    return markup


def show_static_question_category():
    markup = InlineKeyboardMarkup(row_width=True)
    categories = manager.question_category.get_category()
    buttons = [InlineKeyboardButton(text=category[0], callback_data=f"category_{category[0]}") for
               category in categories]
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"main")
    )
    return markup


def show_dynamic_question_category():
    markup = InlineKeyboardMarkup(row_width=True)
    categories = manager.question_category.get_category()
    buttons = [InlineKeyboardButton(text=category[0], callback_data=f"ctg_{category[0]}") for
               category in categories]
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"main")
    )
    return markup


def show_category_answer():
    markup = InlineKeyboardMarkup(row_width=True)
    categories = manager.question_category.get_category()
    buttons = [InlineKeyboardButton(text=category[0], callback_data=f"acategory_{category[0]}") for
               category in categories]
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Все категории", callback_data=f"allcateg"),
        InlineKeyboardButton(text="Назад", callback_data=f"main")
    )
    return markup


def show_category_questions(category_name):
    markup = InlineKeyboardMarkup(row_width=True)
    questions = manager.dynamic_question.get_dynamic_question_by_category(category_name)
    for question in questions:
        text1 = " ".join(question[0:2])
        text1 += " " + question[3]
        # text1 += " " + question[6][:50]
        markup.add(
            InlineKeyboardButton(text=text1, callback_data=f"?")
        )
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"main")
    )
    return markup


def show_subcategories(category_id):
    markup = InlineKeyboardMarkup(row_width=True)
    subcategories = manager.question_subcategory.get_subcategories_by_category_id(category_id)
    buttons = [InlineKeyboardButton(text=subcategory[1], callback_data=f"subcat_{subcategory[0]}") for subcategory in subcategories]
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"faq")
    )
    return markup


def back_main():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"main")
    )
    return markup


def back_static_categories():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"faq")
    )
    return markup


def back_dynamic_categories():
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"ask")
    )
    return markup


# --- Как добраться до ... ---

def how_to_get_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="До корпуса", callback_data=f"way_campus"))
    markup.add(InlineKeyboardButton(text="До общежития", callback_data=f"way_dorm"))
    markup.add(InlineKeyboardButton(text="Назад", callback_data=f"main"))
    return markup


def campuses_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Корпус на Большой Семёновской", callback_data=f"camp_bs"))
    markup.add(InlineKeyboardButton(text="Корпус на Автозаводской", callback_data=f"camp_avto"))
    markup.add(InlineKeyboardButton(text="Корпус на Павла Корчагина", callback_data=f"camp_pk"))
    markup.add(InlineKeyboardButton(text="Корпус на Михалковской", callback_data=f"camp_mikh"))
    markup.add(InlineKeyboardButton(text="Корпус на Прянишникова", callback_data=f"camp_pry"))
    markup.add(InlineKeyboardButton(text="Назад", callback_data=f"way"))
    return markup


def dorms_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    # 1..11 buttons
    for i in range(1, 12):
        markup.add(InlineKeyboardButton(text=f"{i} общежитие", callback_data=f"dorm_{i}"))
    markup.add(InlineKeyboardButton(text="Назад", callback_data=f"way"))
    return markup

