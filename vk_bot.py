import os
import random
import re

import vk_api

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from dotenv import load_dotenv


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


if __name__ == "__main__":
    load_dotenv()

    vk_token = os.getenv("VK_TOKEN")
    quiz_questions_file = os.getenv("QUIZ_QUESTIONS_FILE")

    questions_and_answers = get_questions_and_answers(quiz_questions_file)

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
                answer = questions_and_answers[randome_question]
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
                answer = questions_and_answers[randome_question]
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
