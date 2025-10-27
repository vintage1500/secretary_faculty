from telebot.types import Message
from data.loader import bot, api
from keyboards.default import registration_menu
from keyboards.inline import start_menu, start_administrator_menu


@bot.message_handler(commands=['start'], chat_types=['private'])
def start(message: Message):
    chat_id = message.chat.id
    text = "Здравствуйте"

    # Проверяем, есть ли пользователь
    first_name = api.get_first_name(chat_id)
    user_admin = api.get_is_user_administrator(chat_id)

    if not first_name:
        text += ". Перед использованием необходимо пройти регистрацию.\n"
        bot.send_message(chat_id, text, reply_markup=registration_menu())
        return

    if user_admin:
        text += f", {first_name}. У вас роль администратора!"
        bot.send_message(chat_id, text, reply_markup=start_administrator_menu())
    else:
        text += (
            f", {first_name}, я чат-бот, созданный в рамках учебного проекта "
            f"«Чат-боты для Московского Политеха». Моя задача — помочь вам быстро "
            f"получать нужную информацию и решать вопросы в удобном формате."
        )
        bot.send_message(chat_id, text, reply_markup=start_menu())
