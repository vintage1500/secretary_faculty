from telebot.types import Message
from data.loader import bot, manager
from keyboards.inline import start_menu, start_administrator_menu, registration_menu


@bot.message_handler(commands=['start'], chat_types='private')
def start(message: Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    text = f"Привет, {first_name}"
    us_ex = manager.user.user_exists(chat_id)
    user_administrator = manager.user.get_is_user_administrator(chat_id)
    if user_administrator is None or not user_administrator[0]:
        if us_ex:
            text += ". Вы вошли в систему"
            bot.send_message(chat_id, text, reply_markup=start_menu())
        else:
            text += ". Пройдите регистрацию"
            bot.send_message(chat_id, text, reply_markup=registation_menu(chat_id))
    else:
        text += ". У вас роль администратора!"
        bot.send_message(chat_id, text, reply_markup=start_administrator_menu())
