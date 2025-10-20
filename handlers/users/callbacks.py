import os
import glob
from telebot.types import CallbackQuery, Message, InputMediaPhoto
from telebot.apihelper import ApiTelegramException
from data.loader import bot, manager
from keyboards.default import registration_menu
from keyboards.inline import *


@bot.callback_query_handler(func=lambda call: "main" in call.data)
def back_to_main_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    first_name = manager.user.get_first_name(chat_id)
    text = f"Здравствуйте"
    user_administrator = manager.user.get_is_user_administrator(chat_id)
    if user_administrator is None or user_administrator[0] is False:
        if first_name:
            text += f", {first_name[0]}. Вы вошли в систему"
            bot.edit_message_text(
                text, chat_id, callback.message.message_id, reply_markup=start_menu()
            )
        else:
            text += ". Пройдите регистрацию"
            bot.send_message(chat_id, text, reply_markup=registration_menu())
    else:
        text += f", {first_name[0]}. У вас роль администратора!"
        bot.edit_message_text(
            text,
            chat_id,
            callback.message.message_id,
            reply_markup=start_administrator_menu(),
        )


@bot.callback_query_handler(func=lambda call: "faq" in call.data)
def show_faq_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text(
        "Часто задаваемые вопросы (FAQ)\n\nВыберите категорию вашего вопроса",
        chat_id,
        callback.message.message_id,
        reply_markup=show_static_question_category(),
    )


@bot.callback_query_handler(func=lambda call: call.data == "way")
def show_way_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    safe_edit_text(
        chat_id,
        callback.message.message_id,
        "Как добраться до...\n\nВыберите направление",
        reply_markup=how_to_get_menu(),
    )


@bot.callback_query_handler(func=lambda call: "way_campus" in call.data)
def show_campuses(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    safe_edit_text(
        chat_id,
        callback.message.message_id,
        "Как добраться до корпуса...\n\nВыберите корпус",
        reply_markup=campuses_menu(),
    )


@bot.callback_query_handler(func=lambda call: "way_dorm" in call.data)
def show_dorms_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    safe_edit_text(
        chat_id,
        callback.message.message_id,
        "Как добраться до общежития...\n\nВыберите общежитие",
        reply_markup=dorms_menu(),
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("dorm_"))
def show_dorm_info(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    dorm_num = callback.data.split("_")[1]
    info = {
        "1": (
            "1 общежитие:\n\n"
            "Адрес: ул. Малая Семёновская, д. 12\n"
            "Метро: Электрозаводская\n\n"
            "Общая информация: максимально удобно к корпусу 'На Большой Семёновской'.\n"
            "Тип: блочный — по 2 комнаты в блоке с санузлом и душевой, кухня общая на этаже.\n"
            "Проживающих в блоке: 5\n"
            "Инфраструктура: коворкинг, тренажерный зал, прачечная, спортивная площадка, бесплатный Wi‑Fi."
        ),
        "2": (
            "2 общежитие:\n\n"
            "Адрес: ул. 7‑я Парковая, д 9/26\n"
            "Метро: Первомайская\n\n"
            "Тип: коридорный — раздельные комнаты вдоль коридора, санитарный узел и кухня на этаже, общая душевая.\n"
            "Проживающих в комнате: 3\n"
            "Инфраструктура: коворкинг, тренажерный зал, прачечная, спортивная площадка, бесплатный Wi‑Fi."
        ),
        "3": (
            "3 общежитие:\n\n"
            "Адрес: ул. 1‑я Дубровская, д. 16А, стр. 2\n"
            "Метро: Дубровка\n\n"
            "Тип: коридорный — раздельные комнаты вдоль коридора, санитарный узел и кухня на этаже, общая душевая.\n"
            "Проживающих в комнате: 3\n"
            "Инфраструктура: коворкинг, прачечная, бесплатный Wi‑Fi."
        ),
        "4": (
            "4 общежитие:\n\n"
            "Адрес: ул. 800‑летия Москвы, д. 28, к. 1\n"
            "Метро: Яхромская / МЦД‑1 Бескудниково\n\n"
            "Тип: квартирный — по 1‑3 комнаты в блоке с санузлом, душевой и кухней.\n"
            "Проживающих в квартире: 3‑7\n"
            "Инфраструктура: прачечная, коворкинг, бесплатный Wi‑Fi."
        ),
        "5": (
            "5 общежитие:\n\n"
            "Адрес: ул. Михалковская, д. 7, к. 3\n"
            "Метро: МЦК Коптево\n\n"
            "Тип: блочный — по 2 комнаты в блоке с санузлом и душевой, кухня общая на этаже.\n"
            "Проживающих в блоке: 5\n"
            "Инфраструктура: коворкинг, прачечная, бесплатный Wi‑Fi."
        ),
        "6": (
            "6 общежитие:\n\n"
            "Адрес: ул. Бориса Галушкина, д. 9\n"
            "Метро: ВДНХ\n\n"
            "Тип: блочный — по 2 комнаты в блоке с санузлом и душевой, кухня общая на этаже.\n"
            "Проживающих в блоке: 4‑6\n"
            "Инфраструктура: коворкинг, тренажерный зал, прачечная, бесплатный Wi‑Fi."
        ),
        "7": (
            "7 общежитие:\n\n"
            "Адрес: ул. Павла Корчагина, д. 20А, к. 3\n"
            "Метро: ВДНХ\n\n"
            "Тип: коридорный — раздельные комнаты вдоль коридора, санузел и кухня на этаже, общая душевая.\n"
            "Проживающих в комнате: 3\n"
            "Инфраструктура: комната самоподготовки, прачечная, бесплатный Wi‑Fi."
        ),
        "8": (
            "8 общежитие:\n\n"
            "Адрес: Рижский проезд, д. 15, к. 2\n"
            "Метро: ВДНХ\n\n"
            "Тип: квартирный — по 2 комнаты в блоке с санузлом, душевой и кухней.\n"
            "Проживающих в квартире: 5‑6\n"
            "Инфраструктура: прачечная, спортивный зал, бесплатный Wi‑Fi."
        ),
        "9": (
            "9 общежитие:\n\n"
            "Адрес: Рижский проезд, д. 15, к. 1\n"
            "Метро: ВДНХ\n\n"
            "Тип: квартирный/коридорный — информация будет уточнена.\n"
            "Инфраструктура: прачечная, бесплатный Wi‑Fi."
        ),
        "10": (
            "10 общежитие:\n\n"
            "Адрес: 1‑й Балтийский переулок, д. 6/21, к. 3\n"
            "Метро: Сокол\n\n"
            "Тип: смешанный коридорный и блочный. Коридорный — комнаты вдоль коридора, санузел, душевая и кухня на этаже.\n"
            "Блочный — по 2 комнаты в блоке с санузлом и душевой, кухня общая на этаже.\n"
            "Проживающих в комнате: 1‑2\n"
            "Инфраструктура: коворкинг, прачечная, бесплатный Wi‑Fi."
        ),
        "11": (
            "11 общежитие:\n\n"
            "Адрес: улица Павла Корчагина, 22Ак2\n"
            "Метро: ВДНХ\n\n"
            "Тип: повышенной комфортности, коридорный — раздельные комнаты вдоль коридора, санузел, душевая и кухня на каждом этаже.\n"
            "Проживающих в комнате: 3\n"
            "Инфраструктура: комната самоподготовки, прачечная, бесплатный Wi‑Fi."
        ),
    }
    text = info.get(dorm_num, "Информация будет добавлена позже.")
    _send_or_edit_with_media(
        chat_id,
        callback.message.message_id,
        text,
        "dorms",
        f"dorm_{dorm_num}",
        dorms_menu(),
    )


@bot.callback_query_handler(
    func=lambda call: call.data
    in ["camp_bs", "camp_avto", "camp_pk", "camp_mikh", "camp_pry"]
)
def show_campus_info(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    data = callback.data
    if data == "camp_bs":
        text = (
            "Корпус на Большой Семёновской:\n\n"
            "Адрес: ул. Б. Семёновская, д. 38.\n"
            "Метро: Электрозаводская\n\n"
            "Как пройти от метро до корпуса: см. маршрут на скриншоте.\n\n"
            "Карта подкорпусов: см. скриншот."
        )
    elif data == "camp_avto":
        text = (
            "Корпус на Автозаводской:\n\n"
            "Адрес: ул. Автозаводская, д. 16.\n"
            "Метро: Автозаводская\n\n"
            "Пешком: 1 выход из метро Автозаводская.\n"
            "На автобусе: 3 выход из метро Автозаводская → автобусы 766, 944, с799 → остановки 'Парк Легенд' или 'ТЦ Ривьера'."
        )
    elif data == "camp_pk":
        text = (
            "Корпус на Павла Корчагина:\n\n"
            "Адрес: ул. Павла Корчагина, 22.\n"
            "Метро: ВДНХ\n\n"
            "Пешком: 4 выход из метро ВДНХ.\n"
            "На автобусе: 4 выход → автобус 378 → остановка 'Школа'.\n"
            "Электричка (Ярославское направление): станция 'Маленковская'."
        )
    elif data == "camp_mikh":
        text = (
            "Корпус на Михалковской:\n\n"
            "Адрес: ул. Михалковская, 7.\n"
            "Метро: МЦК Коптево\n\n"
            "Пешком: 2 выход из метро Коптево.\n"
            "На автобусе: от 'Проезд Черепановых' автобусы 72, 427, 801 → 'Политехнический университет'.\n"
            "На трамвае: от 'Михалково 2А' трамвай 29 → 'Политехнический университет'."
        )
    else:
        text = (
            "Корпус на Прянишникова:\n\n"
            "Адрес: ул. Прянишникова, 2А.\n"
            "Метро: МЦК Коптево\n\n"
            "Как пройти от метро до корпуса:\n"
            "Пешком: 2 выход из метро Коптево."
        )
    _send_or_edit_with_media(
        chat_id, callback.message.message_id, text, "campuses", data, campuses_menu()
    )


def _send_or_edit_with_media(
    chat_id: int, message_id: int, text: str, subdir: str, prefix: str, reply_markup
):
    """Отправляет или редактирует сообщение с медиа (если есть) и кнопками"""
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "media", subdir)
    )
    print(f"[DEBUG] Looking for media in: {base_dir}")
    print(f"[DEBUG] Prefix: {prefix}")

    patterns = [
        os.path.join(base_dir, f"{prefix}_*.{ext}")
        for ext in ("jpg", "jpeg", "png", "webp")
    ]
    # Доп. варианты имён для удобства (напр. БС1.jpg / БС2.jpg для camp_bs, ОБ1.jpg для dorm_1)
    alt_prefixes = {
        "camp_bs": ["БС1", "БС2"],
        "camp_avto": ["АВ1", "АВ2"],
        "camp_pk": ["ПК1", "ПК2", "ПК3"],
        "camp_mikh": ["Мих"],
        "camp_pry": ["ПР1", "ПР2", "ПР3"],
        # Общежития
        "dorm_1": ["ОБ1"],
        "dorm_2": ["ОБ2"],
        "dorm_3": ["ОБ3"],
        "dorm_4": ["ОБ4"],
        "dorm_5": ["ОБ5"],
        "dorm_6": ["ОБ6"],
        "dorm_7": ["ОБ7"],
        "dorm_8": ["ОБ8"],
        "dorm_9": ["ОБ9"],
        "dorm_10": ["ОБ10"],
        "dorm_11": ["ОБ11"],
    }
    if prefix in alt_prefixes:
        for alt in alt_prefixes[prefix]:
            for ext in ("jpg", "jpeg", "png", "webp"):
                patterns.append(os.path.join(base_dir, f"{alt}.{ext}"))
                patterns.append(os.path.join(base_dir, f"{alt}_*.{ext}"))
                patterns.append(os.path.join(base_dir, f"{alt}.*.{ext}"))

    print(f"[DEBUG] Patterns: {patterns}")
    file_paths = []
    for pattern in patterns:
        file_paths.extend(glob.glob(pattern))
    file_paths.sort()
    print(f"[DEBUG] Found files: {file_paths}")

    # Если нет медиа - проверяем, можем ли мы редактировать текст или нужно удалить и создать новое
    if not file_paths:
        print(f"[DEBUG] No media files found for {prefix}")
        # Пробуем отредактировать, если не получается - удаляем и отправляем новое
        try:
            safe_edit_text(chat_id, message_id, text, reply_markup=reply_markup)
            return
        except Exception as e:
            print(f"[DEBUG] Could not edit text (maybe photo message?): {e}")
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e2:
                print(f"[DEBUG] Could not delete message: {e2}")
            bot.send_message(chat_id, text, reply_markup=reply_markup)
            return

    # Если есть медиа - удаляем старое сообщение и отправляем новое с фото
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"[DEBUG] Could not delete message: {e}")

    # Отправляем все фото вместе в одном альбоме
    try:
        if len(file_paths) == 1:
            # Если одно фото - отправляем с текстом и кнопками
            with open(file_paths[0], "rb") as fh:
                bot.send_photo(chat_id, fh, caption=text, reply_markup=reply_markup)
        else:
            # Если несколько фото - отправляем альбомом, последнее с текстом и кнопками
            media = []
            open_files = []
            try:
                # Все фото кроме последнего - без caption
                for fp in file_paths[:-1]:
                    f = open(fp, "rb")
                    open_files.append(f)
                    media.append(InputMediaPhoto(f))

                # Последнее фото с текстом
                f = open(file_paths[-1], "rb")
                open_files.append(f)
                media.append(InputMediaPhoto(f, caption=text))

                # Отправляем альбом
                messages = bot.send_media_group(chat_id, media)

                # К последнему сообщению в альбоме добавляем кнопки
                if messages and len(messages) > 0:
                    last_msg = messages[-1]
                    try:
                        bot.edit_message_reply_markup(
                            chat_id, last_msg.message_id, reply_markup=reply_markup
                        )
                    except Exception as e:
                        print(f"[DEBUG] Could not add buttons to media group: {e}")
                        # Отправляем кнопки отдельным сообщением
                        bot.send_message(
                            chat_id, "Выберите действие:", reply_markup=reply_markup
                        )
            finally:
                for f in open_files:
                    try:
                        f.close()
                    except Exception:
                        pass
    except Exception as e:
        print(f"[DEBUG] Error sending media: {e}")
        # Fallback на текст
        bot.send_message(chat_id, text, reply_markup=reply_markup)


def safe_edit_text(chat_id: int, message_id: int, text: str, reply_markup=None):
    try:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=reply_markup)
    except ApiTelegramException as e:
        if "message is not modified" in str(e):
            # Ignore re-editing with the same content/markup
            return
        raise


@bot.callback_query_handler(func=lambda call: "category" in call.data)
def show_subcategory(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, category_name = callback.data.split("_")
    if category_name == "Бланки заявлений":
        bot.edit_message_text(
            """
Бланки заявлений
        
Для получения актуальных бланков заявлений необходимо выполнить следующие шаги: 

1. Перейти в личный кабинет и выбрать «Старый дизайн». 
2. В разделе «Категории» найти и открыть «Бланки заявлений». 
3. Ознакомиться со списком актуальных бланков для заявлений. 

Вы можете выбрать необходимый бланк и использовать его.        
""",
            chat_id,
            callback.message.message_id,
            reply_markup=back_static_categories(),
        )
    else:
        category_id = manager.question_category.get_category_id_by_name(category_name)[
            0
        ]
        bot.edit_message_text(
            f"{category_name}\n\nВыберите подкатегорию",
            chat_id,
            callback.message.message_id,
            reply_markup=show_subcategories(category_id),
        )


@bot.callback_query_handler(func=lambda call: "subcat" in call.data)
def show_subcategory_question_description(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, subcategory_id = callback.data.split("_")
    question_info = (
        manager.question_subcategory.get_subcategories_description_by_subcategory_id(
            subcategory_id
        )[0]
    )
    string = question_info[0] + "\n\n" + question_info[1]
    bot.edit_message_text(
        string,
        chat_id,
        callback.message.message_id,
        reply_markup=back_static_categories(),
    )


@bot.callback_query_handler(func=lambda call: "profile" in call.data)
def show_profile(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    user_info = manager.user.get_full_user_info(chat_id)
    string = (
        f"Профиль\n\nПолное имя: {user_info[0]} {user_info[1]} {user_info[2]}\n"
        f"Группа: {user_info[3]}"
    )
    if user_info[4]:
        string += "\nВы являетесь администратором"
    bot.edit_message_text(
        string, chat_id, callback.message.message_id, reply_markup=back_main()
    )


@bot.callback_query_handler(func=lambda call: "rules" in call.data)
def show_rules(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    string = (
        "Правила\n\n🔖 Используя сервис Секретарь Факультета, Вы автоматически принимаете "
        "и соглашаетесь с данными правилами* "
        "\n\nДанный бот, созданный в рамках учебного проекта «Чат-боты для Московского Политеха». "
        "В настоящее время он находится на этапе разработки и тестирования, поэтому его"
        " функциональность может дополняться и улучшаться."
    )
    bot.edit_message_text(
        string, chat_id, callback.message.message_id, reply_markup=back_main()
    )


@bot.callback_query_handler(func=lambda call: "ask" in call.data)
def start_ask_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text(
        f"Задать вопрос\n\nВыберите категорию вопроса",
        chat_id,
        callback.message.message_id,
        reply_markup=show_dynamic_question_category(),
    )


@bot.callback_query_handler(func=lambda call: "ctg" in call.data)
def start_ask_question_ctg(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, category_name = callback.data.split("_")
    bot.edit_message_text(
        f"Задать вопрос. Категория {category_name}\n\nВведите вопрос ОДНИМ сообщением!\n",
        chat_id,
        callback.message.message_id,
        reply_markup=back_dynamic_categories(),
    )
    bot.register_next_step_handler(
        callback.message, get_new_question, callback.message.id, category_name
    )


def get_new_question(message: Message, old_message_id, category_name):
    chat_id = message.chat.id
    question_text = message.text
    student_id = manager.user.get_user_id(chat_id)
    category_id = manager.question_category.get_category_id_by_name(category_name)

    if student_id and category_id:
        manager.dynamic_question.add_dynamic_question(
            student_id[0], question_text, category_id[0]
        )
        bot.delete_message(chat_id, old_message_id)
        bot.send_message(
            chat_id,
            "Вопрос успешно добавлен в базу данных. Вы возвращены в систему",
            reply_markup=start_menu(),
        )
    else:
        bot.send_message(
            chat_id,
            "Ошибка: не удалось получить данные пользователя или категории. Попробуйте еще раз.",
            reply_markup=start_menu(),
        )


@bot.callback_query_handler(func=lambda call: "answer" in call.data)
def start_answer_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text(
        "Ответить на вопросы\n\nВыберите категорию",
        chat_id,
        callback.message.message_id,
        reply_markup=show_category_answer(),
    )


@bot.callback_query_handler(func=lambda call: "acategory" in call.data)
def continue_answer_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, category_name = callback.data.split("_")
    questions = manager.dynamic_question.get_dynamic_question_by_category(category_name)
    for question in questions:
        text = " ".join(question[0:2])
        text += " " + question[3] + " " + question[6][:10]
        print(text)
    # print(questions[0][6][:20])
    # q = [print(" ".join(question[0:2]), question[3], question[6][:10]) for question in questions]
    bot.edit_message_text(
        f"Ответить на вопросы. Категория {category_name}\n\nВыберите студента, которому ответить",
        chat_id,
        callback.message.message_id,
        reply_markup=show_category_questions(category_name),
    )


@bot.callback_query_handler(func=lambda call: "telephone" in call.data)
def show_telephones(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    string = f"""
Телефонный справочник    

Многофункциональный центр (ЦРС) на Большой Семеновской:
Аудитория: В-207
Телефон: +74952230523, доб. 1105, 1175, 1215, 1375
E-mail: crs-bs@mospolytech.ru

Многофункциональный центр (ЦРС) на Прянишникова:
Аудитория: ПР1311
Телефон: +74952230523, доб. 4056, 4059, 4060
E-mail: crs-pryaniki@mospolytech.ru

Мобилизационный отдел: 
Начальник: Колесников Валерий Алексеевич
Адрес: г. Москва, ул. Б. Семёновская, 38, корп. Н
Аудитория: Н-517
Телефон: +74952230523, доб. 1025

Студенческий городок:
Директор: Лукашова Марина Ивановна
Телефон: +74952230523

Профсоюзная организация: 
Адрес: г. Москва, ул. Б. Семёновская, 38, корп. В
Аудитория: В-202
Телефон: +74952230531
Почта: profkom@mospolytech.ru

Бухгалтерия:
Адрес: г. Москва, ул. Б. Семёновская, 38, корп. А
Аудитория: А-307

Проектная деятельность:
Начальник : Петухов Иван Сергеевич
Адрес: г. Москва, ул. Б. Семёновская, 38, корп. А
Аудитория А-102
Телефон: +74952230523 доб. 1539
Почта: cpd@mospolytech.ru


Общее:
Контакт-центр:
+74952230523
+74952763736
Часы работы:
Пн. — Чт.: 9:00 - 21:00
Пт: 9:00 - 20:00
Сб. — Вс.: 9:30 - 17:15

Общие вопросы (кроме вопросов о поступлении):
mospolytech@mospolytech.ru
"""
    bot.edit_message_text(
        string, chat_id, callback.message.id, reply_markup=back_main()
    )
