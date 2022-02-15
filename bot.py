import os
import random
import re

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


def start(bot, update):
    custom_keyboard = [
        ["Новый вопрос", "Сдаться"],
        ["Мой счет"],
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Я бот для викторин!",
        reply_markup=reply_markup,
    )


def help(bot, update):
    update.message.reply_text("Help!")


def echo(bot, update):
    # update.message.reply_text(update.message.text)
    randome_question = random.choice(list(questions_and_answers.keys()))
    if update.message.text == "Новый вопрос":
        update.message.reply_text(randome_question)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv()

    global questions_and_answers

    quiz_questions_file = os.getenv("QUIZ_QUESTIONS_FILE")
    telegram_token = os.getenv("TELEGRAM_TOKEN")

    questions_and_answers = get_questions_and_answers(quiz_questions_file)

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
