from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, api
from keyboards.default import registration_menu
from keyboards.inline import show_static_question_category, start_menu


@bot.message_handler(func=lambda msg: msg.text == "Пройти регистрацию")
def register(message: Message):
    chat_id = message.chat.id
    if api.user_exists(chat_id):
        bot.send_message(chat_id, "Вы уже зарегистрированы ✅")
    else:
        bot.send_message(
            chat_id,
            "Введите свои ФИО и номер группы одним сообщением.\n\n"
            "Пример:\nИванов Иван Иванович\n222-222",
            reply_markup=ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, get_new_user)


def get_new_user(message: Message):
    chat_id = message.chat.id
    try:
        student_info = message.text.split()
        last_name = student_info[0]
        first_name = student_info[1]
        patronymic = student_info[2]
        us_group = student_info[3]
        username = message.from_user.username

        if api.add_user(last_name, first_name, patronymic, us_group, username, chat_id):
            bot.send_message(chat_id, f"Регистрация прошла успешно. Здравствуйте, {first_name}!",
                             reply_markup=start_menu())
        else:
            bot.send_message(chat_id, "Ошибка регистрации. Попробуйте снова.", reply_markup=registration_menu())

    except Exception:
        bot.send_message(
            chat_id,
            "❌ Проверьте корректность введённых данных и повторите попытку.",
            reply_markup=registration_menu()
        )


@bot.message_handler(func=lambda msg: msg.text == "Отмена")
def cancel_main_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Регистрация отменена. Для начала введите /start",
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda msg: msg.text == "Часто задаваемые вопросы")
def start_faq(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Выберите нужную вам сферу 👇", reply_markup=show_static_question_category())


def get_new_question(message: Message):
    chat_id = message.chat.id
    question_text = message.text
    parts = question_text.split("\n")

    if len(parts) < 3:
        bot.send_message(chat_id, "❌ Неверный формат. Повторите попытку.", reply_markup=start_menu())
        return

    student_name, student_group, student_question = parts[:3]
    username = message.from_user.username
    user_id = api.get_user_id(chat_id)

    if not user_id:
        bot.send_message(chat_id, "Пользователь не найден. Пройдите регистрацию.", reply_markup=registration_menu())
        return

    if api.add_dynamic_question(user_id, student_question, 1):  # 1 — временная категория
        bot.send_message(chat_id, "✅ Вопрос успешно добавлен в базу данных", reply_markup=start_menu())
    else:
        bot.send_message(chat_id, "Ошибка при отправке вопроса.", reply_markup=start_menu())
