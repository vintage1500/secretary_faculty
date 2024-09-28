from telebot.types import Message
from data.loader import bot, manager


@bot.message_handler(func=lambda msg: msg.text == "Часто задаваемые вопросы")
def start_register(message: Message):
    chat_id = message.chat.id


@bot.message_handler(func=lambda msg: msg.text == "Задать вопрос")
def start_ask_question(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Введите интересующий вас вопрос\n"
                              f"В запросе обязательно должны в такой форме:\n"
                              f"Иванов Иван\n222-222\n*Вопрос*\n"
                              f"Все должно быть одним сообщением!")
    bot.register_next_step_handler(message, get_new_question, message.text)


def get_new_question(message: Message, text):
    chat_id = message.chat.id
    print(text)

    # bot.register_next_step_handler(message, request_new_question, message.text)
    request_new_question(message, message.text)


def request_new_question(message: Message, question_text):
    chat_id = message.chat.id
    student_info = question_text.split("\n")
    student_name = student_info[0]
    student_group = student_info[1]
    student_question = student_info[2]
    student_username = message.from_user.username
    manager.dynamic_question.add_dynamic_question(student_name, student_group, student_question, student_username, chat_id)
    bot.send_message(chat_id, "Вопрос успешно добавлен в базу данных")


@bot.message_handler(func=lambda msg: msg.text == "Принять запрос")
def start_answer_question(message: Message):
    chat_id = message.chat.id
    unanswered_questions = manager.dynamic_question.get_has_dynamic_question()
    number_of_questions = len(unanswered_questions)
    if number_of_questions == 1:
        question_student_name = unanswered_questions[0][0]
        question_student_group = unanswered_questions[0][1]
        question_description = unanswered_questions[0][2]
        question_username = unanswered_questions[0][3]
        text = (f"Был отправлен вопрос от: {question_student_name}\n"
                f"Из группы {question_student_group}\n"
                f"Вопрос: {question_description}\n"
                f"Ссылка на задающего: @{question_username}\n")
        bot.send_message(chat_id, text)

    elif number_of_questions == 0 or number_of_questions is None:
        bot.send_message(chat_id, "Нет сообщений")
    elif number_of_questions > 1:
        pass
    else:
        print("Error in function start_answer_question")
        bot.send_message(chat_id, "Error in function start_answer_question")