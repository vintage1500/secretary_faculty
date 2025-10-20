
# from data.loader import bot

# import handlers


# if __name__ == '__main__':
#     bot.infinity_polling()

# ВРЕМЕННО закоментировали запуск бота со старыми настройками и функциям
# необходимо в django повторить структуру БД и также прописать 
# взаимодействия к базе данных с помощью REST
# Ниже пока временное решение для тестов работоспособности после слияния ботов

import telebot
import requests
import environ
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Загружаем .env
env = environ.Env()
environ.Env.read_env()

# Инициализация бота
bot = telebot.TeleBot(env('TOKEN'))

# Django API endpoint
DJANGO_API_URL = "http://127.0.0.1:8000/api/questions/create/"

# Храним состояния пользователей
user_states = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Абитуриент", callback_data='applicant'),
        InlineKeyboardButton("Студент", callback_data='student')
    )
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Пожалуйста, выберите ваш статус:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in ['applicant', 'student']:
        user_states[call.from_user.id] = {
            'user_type': call.data,
            'username': call.from_user.username
        }
        bot.send_message(
            call.from_user.id,
            "Спасибо! Теперь напишите ваш вопрос:"
        )
        bot.register_next_step_handler(call.message, save_question)

def save_question(message):
    chat_id = message.chat.id
    try:
        if chat_id in user_states:
            user_type = user_states[chat_id]['user_type']
            username = user_states[chat_id].get('username')
            question_text = message.text.strip()

            if not question_text:
                bot.send_message(chat_id, "Вопрос не может быть пустым. Пожалуйста, напишите ваш вопрос:")
                bot.register_next_step_handler(message, save_question)
                return

            payload = {
                "user_id": chat_id,
                "user_type": user_type,
                "username": username,
                "question": question_text
            }

            response = requests.post(DJANGO_API_URL, json=payload)
            if response.status_code == 201:
                bot.send_message(chat_id, "✅ Ваш вопрос успешно отправлен!\nМы рассмотрим его в ближайшее время.")
            else:
                bot.send_message(chat_id, f"⚠️ Ошибка при отправке вопроса: {response.text}")

            del user_states[chat_id]

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(chat_id, "Произошла ошибка при обработке вашего вопроса. Попробуйте позже.")

print("Бот запущен...")
bot.infinity_polling()
