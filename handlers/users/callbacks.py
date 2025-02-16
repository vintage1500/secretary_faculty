from telebot.types import CallbackQuery, Message
from data.loader import bot, manager
from keyboards.default import registration_menu
from keyboards.inline import show_static_question_category, start_menu, start_administrator_menu, back_main


@bot.callback_query_handler(func=lambda call: "main" in call.data)
def back_to_main_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id

    first_name = callback.message.from_user.first_name
    text = f"Привет, {first_name}"
    us_ex = manager.user.user_exists(chat_id)
    user_administrator = manager.user.get_is_user_administrator(chat_id)
    if user_administrator is None or not user_administrator[0]:
        if us_ex:
            text += ". Вы вошли в систему"
            bot.edit_message_text(text, chat_id, callback.message.message_id, reply_markup=start_menu())
        else:
            text += ". Пройдите регистрацию"
            bot.send_message(text, chat_id, callback.message.message_id,  reply_markup=registration_menu())
    else:
        text += ". У вас роль администратора!"
        bot.send_message(text, chat_id, callback.message.message_id, reply_markup=start_administrator_menu())


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
    string = (f"Имя: {user_info[0]} {user_info[1]} {user_info[2]}\n"
              f"Группа: {user_info[3]}")
    if user_info[4]:
        string += "\nВы являетесь администратором"
    bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=back_main())


@bot.callback_query_handler(func=lambda call: "rules" in call.data)
def show_rules(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    string = "🔖 Используя сервис Секретарь Факультета, Вы автоматически принимаете и соглашаетесь с данными правилами*"
    bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=back_main())


@bot.callback_query_handler(func=lambda call: "ask" in call.data)
def start_ask_question(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    # bot.delete_message(chat_id, callback.message.id)
    bot.edit_message_text(f"Введите интересующий вас вопрос\n"
                              f"В запросе обязательно должны в такой форме:\n"
                              f"Иванов Иван\n222-222\n*Вопрос*\n"
                              f"Все должно быть одним сообщением!",
                          chat_id, callback.message.message_id, reply_markup=back_main())
    bot.register_next_step_handler(callback.message, get_new_question, callback.message.id)


def get_new_question(message: Message, old_message_id):
    chat_id = message.chat.id
    question_text = message.text
    student_info = question_text.split("\n")
    student_name = student_info[0]
    student_group = student_info[1]
    student_question = student_info[2]
    student_username = message.from_user.username
    manager.dynamic_question.add_dynamic_question(student_name, student_group, student_question, student_username,
                                                  chat_id)
    bot.delete_message(chat_id, old_message_id)
    bot.send_message(chat_id, "Вопрос успешно добавлен в базу данных. Вы возвращены в систему",
                     reply_markup=start_menu())
