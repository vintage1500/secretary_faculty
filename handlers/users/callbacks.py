from telebot.types import CallbackQuery, Message
from data.loader import bot, api
from keyboards.default import registration_menu
from keyboards.inline import (
    start_menu,
    start_administrator_menu,
    show_static_question_category,
    back_static_categories,
    show_subcategories,
    back_main,
    show_dynamic_question_category,
    back_dynamic_categories,
    show_category_answer,
    show_category_questions
)


@bot.callback_query_handler(func=lambda call: "main" in call.data)
def back_to_main_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    first_name = api.get_first_name(chat_id)
    is_admin = api.get_is_user_administrator(chat_id)
    text = "Здравствуйте"

    if not first_name:
        bot.send_message(chat_id, text + ". Пройдите регистрацию.", reply_markup=registration_menu())
        return

    if is_admin:
        bot.edit_message_text(
            f"{text}, {first_name}. У вас роль администратора!",
            chat_id, callback.message.message_id, reply_markup=start_administrator_menu()
        )
    else:
        bot.edit_message_text(
            f"{text}, {first_name}. Вы вошли в систему.",
            chat_id, callback.message.message_id, reply_markup=start_menu()
        )


@bot.callback_query_handler(func=lambda call: "faq" in call.data)
def show_faq_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text("Часто задаваемые вопросы (FAQ)\n\nВыберите категорию 👇",
                          chat_id, callback.message.message_id,
                          reply_markup=show_static_question_category())


@bot.callback_query_handler(func=lambda call: "category" in call.data)
def show_subcategory(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, category_name = callback.data.split("_")
    category_id = api.get_category_id_by_name(category_name)
    bot.edit_message_text(
        f"{category_name}\n\nВыберите подкатегорию:",
        chat_id, callback.message.message_id,
        reply_markup=show_subcategories(category_id)
    )


@bot.callback_query_handler(func=lambda call: "subcat" in call.data)
def show_subcategory_question_description(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, subcategory_id = callback.data.split("_")
    info = api.get_subcategory_description(subcategory_id)
    text = f"{info.get('name', '')}\n\n{info.get('description', '')}"
    bot.edit_message_text(text, chat_id, callback.message.message_id, reply_markup=back_static_categories())


@bot.callback_query_handler(func=lambda call: "profile" in call.data)
def show_profile(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    info = api.get_full_user_info(chat_id)
    if not info:
        bot.send_message(chat_id, "Профиль не найден. Пройдите регистрацию.", reply_markup=registration_menu())
        return

    text = (
        f"👤 Профиль\n\n"
        f"ФИО: {info['last_name']} {info['first_name']} {info['patronymic']}\n"
        f"Группа: {info['us_group']}\n"
    )
    if info['administrator']:
        text += "Роль: Администратор"
    bot.edit_message_text(text, chat_id, callback.message.message_id, reply_markup=back_main())


@bot.callback_query_handler(func=lambda call: "ask" in call.data)
def start_ask_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text("📝 Задать вопрос\n\nВыберите категорию:", chat_id, callback.message.message_id,
                          reply_markup=show_dynamic_question_category())


@bot.callback_query_handler(func=lambda call: "ctg" in call.data)
def start_ask_question_ctg(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, category_name = callback.data.split("_")
    bot.edit_message_text(f"Введите вопрос одним сообщением 👇", chat_id,
                          callback.message.message_id, reply_markup=back_dynamic_categories())
    bot.register_next_step_handler(callback.message, get_new_question, callback.message.id, category_name)


def get_new_question(message: Message, old_message_id, category_name):
    chat_id = message.chat.id
    text = message.text
    user_id = api.get_user_id(chat_id)
    category_id = api.get_category_id_by_name(category_name)

    if not user_id:
        bot.send_message(chat_id, "❌ Вы не зарегистрированы. Пройдите регистрацию.", reply_markup=registration_menu())
        return

    if api.add_dynamic_question(user_id, text, category_id):
        bot.delete_message(chat_id, old_message_id)
        bot.send_message(chat_id, "✅ Вопрос успешно добавлен!", reply_markup=start_menu())
    else:
        bot.send_message(chat_id, "Ошибка при добавлении вопроса.", reply_markup=start_menu())


@bot.callback_query_handler(func=lambda call: "answer" in call.data)
def start_answer_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text("📨 Ответить на вопросы\n\nВыберите категорию:", chat_id,
                          callback.message.message_id, reply_markup=show_category_answer())


@bot.callback_query_handler(func=lambda call: "acategory" in call.data)
def continue_answer_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, category_name = callback.data.split("_")
    questions = api.get_dynamic_question_by_category(category_name)

    if not questions:
        bot.edit_message_text(f"Нет вопросов в категории {category_name}.", chat_id,
                              callback.message.message_id, reply_markup=back_main())
        return

    for q in questions:
        text = (f"Вопрос от {q['first_name']} {q['last_name']} ({q['us_group']})\n"
                f"Категория: {q['category']}\n"
                f"Вопрос: {q['description']}")
        bot.send_message(chat_id, text)

    bot.edit_message_text(f"Ответить на вопросы. Категория {category_name}",
                          chat_id, callback.message.message_id,
                          reply_markup=show_category_questions(category_name))
