import os
import random
import re
import redis

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def get_questions_and_answers(filename):
    questions_and_answers = {}
    question_pattern = re.compile("Вопрос \d*:\n")
    answer_pattern = re.compile("Ответ:\n")

    with open(filename, "r", encoding="koi8-r") as file:
        file_contents = file.read()

    for file_section in file_contents.split("\n\n\n"):
        question, answer = None, None
        for question_section in file_section.split("\n\n"):
            if question_pattern.match(question_section):
                question = question_pattern.split(question_section)[1]
            if answer_pattern.match(question_section):
                answer = answer_pattern.split(question_section)[1]
        if (question is not None) and (answer is not None):
            questions_and_answers[question] = answer

    return questions_and_answers


def start(update, context):
    custom_keyboard = [
        ["Новый вопрос", "Сдаться"],
        ["Мой счет"],
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Я бот для викторин!",
        reply_markup=reply_markup,
    )


def help(update, context):
    update.message.reply_text("Help!")


def echo(update, context):
    questions_and_answers = context.bot_data
    randome_question = random.choice(list(questions_and_answers.keys()))

    if update.message.text == "Новый вопрос":
        update.message.reply_text(randome_question)
        context.user_data["current_question"] = randome_question
    else:
        answer = questions_and_answers[context.user_data["current_question"]]
        smart_answer = answer.split("(")[0].split(".")[0]
        if update.message.text == smart_answer:
            update.message.reply_text(
                "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»"
            )
        else:
            update.message.reply_text("Неправильно… Попробуешь ещё раз?")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    quiz_questions_file = os.getenv("QUIZ_QUESTIONS_FILE")
    # redis_host = os.getenv("REDIS_HOST")
    # redis_port = os.getenv("REDIS_PORT")
    # redis_pass = os.getenv("REDIS_PASS")

    # redis_connection = redis.Redis(
    #     host=redis_host, port=redis_port, password=redis_pass, db=0
    # )

    questions_and_answers = get_questions_and_answers(quiz_questions_file)
    # randome_question = random.choice(list(questions_and_answers.keys()))

    # redis_connection.set("1", randome_question)
    # redis_connection.set("2", randome_question)
    #
    # print(redis_connection.get("1"))
    # print(redis_connection.get("2"))

    updater = Updater(telegram_token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    dp.bot_data = questions_and_answers

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
