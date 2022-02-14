import re


def main():
    questions_and_answers = {}
    question_pattern = re.compile("Вопрос \d*:\n")
    answer_pattern = re.compile("Ответ:\n")

    with open("quiz-questions/1vs1201.txt", "r", encoding="koi8-r") as file:
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

    print(questions_and_answers)


if __name__ == "__main__":
    main()
