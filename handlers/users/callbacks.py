from telebot.types import CallbackQuery, Message
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
            bot.edit_message_text(text, chat_id, callback.message.message_id, reply_markup=start_menu())
        else:
            text += ". Пройдите регистрацию"
            bot.send_message(text, chat_id, callback.message.message_id,  reply_markup=registration_menu())
    else:
        text += f", {first_name[0]}. У вас роль администратора!"
        bot.edit_message_text(text, chat_id, callback.message.message_id, reply_markup=start_administrator_menu())


@bot.callback_query_handler(func=lambda call: "faq" in call.data)
def show_faq_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text("Часто задаваемые вопросы (FAQ)\n\nВыберите категорию вашего вопроса",
                          chat_id, callback.message.message_id,
                          reply_markup=show_static_question_category())


@bot.callback_query_handler(func=lambda call: "profile" in call.data)
def show_profile(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    user_info = manager.user.get_full_user_info(chat_id)
    string = (f"Профиль\n\nПолное имя: {user_info[0]} {user_info[1]} {user_info[2]}\n"
              f"Группа: {user_info[3]}")
    if user_info[4]:
        string += "\nВы являетесь администратором"
    bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=back_main())


@bot.callback_query_handler(func=lambda call: "rules" in call.data)
def show_rules(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    string = "Правила\n\n🔖 Используя сервис Секретарь Факультета, Вы автоматически принимаете " \
             "и соглашаетесь с данными правилами*"
    bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=back_main())


@bot.callback_query_handler(func=lambda call: "ask" in call.data)
def start_ask_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text(f"Задать вопрос\n\nВыберите категорию вопроса", chat_id, callback.message.message_id,
                          reply_markup=show_dynamic_question_category())


@bot.callback_query_handler(func=lambda call: "ctg" in call.data)
def start_ask_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, category_name = callback.data.split("_")
    bot.edit_message_text(f"Задать вопрос. Категория {category_name}\n\nВведите вопрос ОДНИМ сообщением!\n", chat_id,
                          callback.message.message_id, reply_markup=back_dynamic_categories())
    bot.register_next_step_handler(callback.message, get_new_question, callback.message.id, category_name)


def get_new_question(message: Message, old_message_id, category_name):
    chat_id = message.chat.id
    question_text = message.text
    student_id = manager.user.get_user_id(chat_id)
    category_id = manager.question_category.get_category_id_by_name(category_name)
    manager.dynamic_question.add_dynamic_question(student_id, question_text, category_id)
    bot.delete_message(chat_id, old_message_id)
    bot.send_message(chat_id, "Вопрос успешно добавлен в базу данных. Вы возвращены в систему",
                     reply_markup=start_menu())


@bot.callback_query_handler(func=lambda call: "answer" in call.data)
def start_answer_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.edit_message_text("Ответить на вопросы\n\nВыберите категорию", chat_id, callback.message.message_id,
                          reply_markup=show_category_answer())


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
    bot.edit_message_text(f"Ответить на вопросы. Категория {category_name}\n\nВыберите студента, которому ответить",
                          chat_id, callback.message.message_id, reply_markup=show_category_questions(category_name))
