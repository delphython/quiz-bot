import logging
import os
import random

import redis

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

(
    NEW_QUESTION,
    HANDLE_SOLUTION,
    GIVE_UP,
) = range(3)


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

    return NEW_QUESTION


def help(update, context):
    update.message.reply_text("Help!")


def handle_new_question_request(update, context):
    questions_and_answers = context.bot_data
    random_question = random.choice(list(questions_and_answers.keys()))

    update.message.reply_text(randome_question.decode("utf-8"))
    context.user_data["current_question"] = randome_question

    return HANDLE_SOLUTION


def handle_solution_attempt(update, context):
    questions_and_answers = context.bot_data
    answer = questions_and_answers[
        context.user_data["current_question"]
    ].decode("utf-8")
    context.user_data["current_answer"] = answer
    smart_answer = answer.split("(")[0].split(".")[0]

    if update.message.text == smart_answer:
        update.message.reply_text(
            "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»"
        )
        return NEW_QUESTION
    else:
        update.message.reply_text("Неправильно… Попробуешь ещё раз?")
        return GIVE_UP


def handle_give_up(update, context):
    answer = context.user_data["current_answer"]
    update.message.reply_text(f"Правильный ответ: {answer}")

    questions_and_answers = context.bot_data
    randome_question = random.choice(list(questions_and_answers.keys()))

    update.message.reply_text(randome_question.decode("utf-8"))
    context.user_data["current_question"] = randome_question

    return HANDLE_SOLUTION


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    redis_db = os.getenv("REDIS_DB")
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    redis_pass = os.getenv("REDIS_PASS")

    redis_connection = redis.Redis(
        host=redis_host, port=redis_port, password=redis_pass, db=0
    )

    questions_and_answers = redis_connection.hgetall(redis_db)

    updater = Updater(telegram_token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NEW_QUESTION: [
                MessageHandler(
                    Filters.regex("^Новый вопрос$"),
                    handle_new_question_request,
                ),
            ],
            HANDLE_SOLUTION: [
                MessageHandler(Filters.text, handle_solution_attempt),
            ],
            GIVE_UP: [
                MessageHandler(Filters.regex("^Сдаться$"), handle_give_up),
                MessageHandler(Filters.text, handle_solution_attempt),
            ],
        },
        fallbacks=[CommandHandler("exit", exit)],
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    dp.bot_data = questions_and_answers

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
