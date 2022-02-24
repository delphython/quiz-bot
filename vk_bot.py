import os
import random

import redis
import vk_api

from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


def main():
    load_dotenv()

    vk_token = os.getenv("VK_TOKEN")
    redis_db = os.getenv("REDIS_DB")
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    redis_pass = os.getenv("REDIS_PASS")

    redis_connection = redis.Redis(
        host=redis_host, port=redis_port, password=redis_pass, db=0
    )

    questions_and_answers = redis_connection.hgetall(redis_db)

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button("Новый вопрос", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Сдаться", color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()
    keyboard.add_button("Мой счет", color=VkKeyboardColor.NEGATIVE)

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == "/start":
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message="Привет! Я бот для викторин!"
                )
            elif event.text == "Новый вопрос":
                randome_question = random.choice(
                    list(questions_and_answers.keys())
                )
                answer = questions_and_answers[randome_question].decode("utf-8")
                smart_answer = answer.split("(")[0].split(".")[0]
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=randome_question
                )
            elif event.text == "Сдаться":
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=f"Правильный ответ: {answer}"
                )
                randome_question = random.choice(
                    list(questions_and_answers.keys())
                )
                answer = questions_and_answers[randome_question].decode("utf-8")
                smart_answer = answer.split("(")[0].split(".")[0]
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=randome_question
                )
            elif event.text == "Мой счет":
                pass
            else:
                if event.text == smart_answer:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message="Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»"
                    )
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard(),
                        message="Неправильно… Попробуешь ещё раз?"
                    )


if __name__ == "__main__":
    main()
