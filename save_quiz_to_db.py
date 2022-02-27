import argparse
import os
import re

import redis

from dotenv import load_dotenv


def get_questions_and_answers(filename):
    questions_and_answers = {}
    question_pattern = re.compile(r"Вопрос \d*:\n")
    answer_pattern = re.compile(r"Ответ:\n")

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


def main():
    load_dotenv()

    redis_db = os.getenv("REDIS_DB")
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    redis_pass = os.getenv("REDIS_PASS")

    parser = argparse.ArgumentParser(description="Add quiz to database script")

    parser.add_argument(
        "quiz_file_path", help="Path to questions and answers file"
    )

    args = parser.parse_args()

    questions_and_answers = get_questions_and_answers(args.quiz_file_path)

    redis_connection = redis.Redis(
        host=redis_host, port=redis_port, password=redis_pass, db=0
    )

    for question, answer in questions_and_answers.items():
        redis_connection.hset(redis_db, question, answer)


if __name__ == "__main__":
    main()
