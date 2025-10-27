from telebot.types import CallbackQuery, Message

from data.loader import bot, manager
from keyboards.default import registration_menu
from keyboards.inline import *


@bot.callback_query_handler(func=lambda call: "main" in call.data)
def back_to_main_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    first_name = manager.user.get_first_name(chat_id)
    text = "Здравствуйте"
    user_administrator = manager.user.get_is_user_administrator(chat_id)
    if user_administrator is None or user_administrator[0] is False:
        if first_name:
            text += f", {first_name[0]}. Вы вошли в систему"
            bot.edit_message_text(
                text, chat_id, callback.message.message_id, reply_markup=start_menu()
            )
        else:
            text += ". Пройдите регистрацию"
            bot.send_message(
                text,
                chat_id,
                callback.message.message_id,
                reply_markup=registration_menu(),
            )
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
        "Задать вопрос\n\nВыберите категорию вопроса",
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
    manager.dynamic_question.add_dynamic_question(
        student_id, question_text, category_id
    )
    bot.delete_message(chat_id, old_message_id)
    bot.send_message(
        chat_id,
        "Вопрос успешно добавлен в базу данных. Вы возвращены в систему",
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
    string = """
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


TEXTS = {
    "": "В Московском Политехе на очной форме обучения учеба состоит из двух “блоков” - лекции и семинарские занятия (практики и лабораторные работы). Свое расписание Вы можете узнать в личном кабинете по ссылке: https://e.mospolytech.ru/#/schedule/current, или на специализированном сайте ( необходимо ввести номер своей группы): https://rasp.dmami.ru/. В нашем университете действует **шестидневная система обучения** (с понедельника по субботу), об этом далее. ",
    "lections": "**Лекции** в Московском Политехе проходят в **онлайн формате** и, за частую, под них выделенно **от 2х до 3х рабочих дней**. Количество лекций может варьироваться **от одной до четырех в один рабочий день**. Сами лекции проходят в MTS link, но преподаватель может, по своему усмотрению, переносить их на другие платформы. Продолжительность одной лекции составляет 2 академических часа (90 минут - “пара”). Перерывы между парами длятся 10 минут, между 3 и 4 парой перерыв на обед -  40 минут (с 13.50 до 14.30).",
    "seminars": """
**Семинарские занятия** в Московском Политехе проходят в **очном формате**, в неделю может быть **от 2х до 4х очных дней**. **Все дни могут быть в разных корпусах**, обращайте внимание на то, в каком корпусе проходят пары сегодня!! О расположении корпусов вы можете узнать в нашем боте.  

Как определить, в какой корпус необходимо ехать: 

1) Если в расписании у пары стоит приписка “A”, “Б”, “В”, “Н”, “Нд” - Вам необходимо ехать в корпус на Большой Семеновской. 

2) Если в расписании у пары стоит приписка “ПК” - Вам необходимо ехать в корпус на Павла Корчагина. 

3) Если в расписании у пары стоит приписка “АВ” - Вам необходимо ехать в корпус на Автозаводской. 

4) Если в расписании у пары стоит приписка “М” - Вам необходимо ехать в корпус на Михалковская. 
5) Если в расписании у пары стоит приписка “ПР” - Вам необходимо ехать в корпус на Прянишникова. 

Количество очных пар может варьироваться **от одной до четырех в один рабочий день**. Перерывы между парами длятся 10 минут, между 3 и 4 парой перерыв на обед -  40 минут (с 13.50 до 14.30).
    """,
    "lms": """
Занятия также будут проходить с использованием платформы электронного обучения Московского Политеха. Тебе не требуется никакого специального программного обеспечения, достаточно иметь браузер и доступ в интернет. 

Ссылка на ЛМС систему: https://online.mospolytech.ru/ 

Логин и пароль для доступа к ЛМС Вы получите на личную почту. Если возникли сложности с доступом — обратитесь с вопросом на почту lms@mospolytech.ru.  
    """,
}


@bot.callback_query_handler(func=lambda call: "how_learning_goes" in call.data)
def show_learn_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    selected_method = callback.data.removeprefix("how_learning_goes_")
    text = TEXTS[selected_method]
    markup = back_how_to_learn_goes() if selected_method else how_to_learn_goes_markup()

    bot.edit_message_text(text, chat_id, callback.message.id, reply_markup=markup)
