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


def campus_detail_menu(campus_code):
    """Меню для конкретного корпуса с кнопкой маршрута на 2ГИС"""
    markup = InlineKeyboardMarkup(row_width=1)
    
    # Словарь: корпус -> готовая ссылка на 2ГИС
    campus_routes = {
        "camp_bs": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.703957%2C55.781822%3B4504385606385781%7C37.710476%2C55.78147%3B4504235283021850?m=37.707243%2C55.78185%2F15.8",
        "camp_avto": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.657119%2C55.706358%7C37.645242%2C55.704325%3B4504583183265077?m=37.649043%2C55.706373%2F16.9",     # TODO: вставить ссылку
        "camp_pk": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.641507%2C55.821029%3B4504385606385695%7C37.663585%2C55.81965%3B4504583183281145?m=37.660053%2C55.816087%2F16.58",       # TODO: вставить ссылку
        "camp_mikh": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.52277%2C55.839678%7C37.533368%2C55.837456%3B4504583175208509?m=37.528102%2C55.838598%2F15.8%2Fp%2F28.81%2Fr%2F-83.88",     # TODO: вставить ссылку
        "camp_pry": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.520856%2C55.840069%3B4504385655418028%7C37.543955%2C55.833841%3B4504127908675082?m=37.542243%2C55.83264%2F17.45%2Fr%2F-80.09",      # TODO: вставить ссылку
    }
    
    if campus_code in campus_routes and campus_routes[campus_code]:
        gis_route_url = campus_routes[campus_code]
        markup.add(InlineKeyboardButton(text="📍 Маршрут от метро (2ГИС)", url=gis_route_url))
    
    markup.add(InlineKeyboardButton(text="Назад к списку корпусов", callback_data=f"way_campus"))
    markup.add(InlineKeyboardButton(text="Главное меню", callback_data=f"main"))
    return markup


def dorms_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    # 1..11 buttons
    for i in range(1, 12):
        markup.add(InlineKeyboardButton(text=f"{i} общежитие", callback_data=f"dorm_{i}"))
    markup.add(InlineKeyboardButton(text="Назад", callback_data=f"way"))
    return markup


def dorm_detail_menu(dorm_num):
    """Меню для конкретного общежития с кнопкой маршрута на 2ГИС"""
    markup = InlineKeyboardMarkup(row_width=1)
    
    # Словарь: общежитие -> готовая ссылка на 2ГИС
    dorm_routes = {
        "1": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.705284%2C55.782126%7C37.711146%2C55.784427%3B4504127909067938?m=37.708215%2C55.783206%2F15.8",       # TODO: вставить ссылку (Электрозаводская -> ОБ1)
        "2": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.79939%2C55.794754%3B4504385606390718%7C37.793503%2C55.796371%3B4504127909067939?m=37.795737%2C55.796505%2F17%2Fr%2F-0.93",       # TODO: вставить ссылку (Первомайская -> ОБ2)
        "3": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.675923%2C55.718704%3B4504385606385968%7C37.672202%2C55.723056%3B4504127909205767?m=37.674%2C55.720432%2F15.8%2Fr%2F-0.54",       # TODO: вставить ссылку (Дубровка -> ОБ3)
        "4": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.545519%2C55.879737%3B70030076661221553%7C37.562283%2C55.879494%3B70000001027699005?m=37.554118%2C55.879328%2F15.8%2Fr%2F-0.2",       # TODO: вставить ссылку (МЦД Бескудниково -> ОБ4)
        "5": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.520856%2C55.840069%3B4504385655418028%7C37.534405%2C55.837108%3B4504127909069383?m=37.526253%2C55.839292%2F17.46%2Fp%2F24.28%2Fr%2F-53.78",       # TODO: вставить ссылку (МЦК Коптево -> ОБ5)
        "6": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.641507%2C55.821029%3B4504385606385695%7C37.65479%2C55.824787%3B70000001025324461?m=37.653851%2C55.823493%2F17.59%2Fp%2F24.28%2Fr%2F-42.36",       # TODO: вставить ссылку (ВДНХ -> ОБ6)
        "7": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.641507%2C55.821029%3B4504385606385695%7C37.663605%2C55.818701%3B70000001059827658?m=37.651486%2C55.818884%2F15.8%2Fp%2F24.28%2Fr%2F-41.18",       # TODO: вставить ссылку (ВДНХ -> ОБ7)
        "8": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.641507%2C55.821029%3B4504385606385695%7C37.664674%2C55.818834%3B70000001034592700?m=37.653494%2C55.819977%2F15.8%2Fp%2F24.28%2Fr%2F-41.18",       # TODO: вставить ссылку (ВДНХ -> ОБ8)
        "9": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.641507%2C55.821029%3B4504385606385695%7C37.664284%2C55.818393%3B70000001033276147?m=37.651488%2C55.818809%2F15.8%2Fp%2F24.28%2Fr%2F-41.18",       # TODO: вставить ссылку (ВДНХ -> ОБ9)
        "10": "https://2gis.ru/moscow/directions/tab/pedestrian/points/37.515243%2C55.805218%3B4504385606390709%7C37.520394%2C55.809658%3B70000001007496358?m=37.517897%2C55.807415%2F15.8%2Fp%2F24.28%2Fr%2F-26.06",      # TODO: вставить ссылку (Сокол -> ОБ10)
        "11": "https://2gis.ru/moscow/directions/points/37.641507%2C55.821029%3B4504385606385695%7C37.664285%2C55.819368%3B70000001102436524?m=37.652984%2C55.8191%2F15.75%2Fp%2F24.28%2Fr%2F-17.48",      # TODO: вставить ссылку (ВДНХ -> ОБ11)
    }
    
    if dorm_num in dorm_routes and dorm_routes[dorm_num]:
        gis_route_url = dorm_routes[dorm_num]
        markup.add(InlineKeyboardButton(text="📍 Маршрут от метро (2ГИС)", url=gis_route_url))
    
    markup.add(InlineKeyboardButton(text="Назад к списку общежитий", callback_data=f"way_dorm"))
    markup.add(InlineKeyboardButton(text="Главное меню", callback_data=f"main"))
    return markup

