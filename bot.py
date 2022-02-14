def main():
    with open("quiz-questions/1vs1200.txt", "r", encoding="koi8-r") as file:
        file_contents = file.read()

    for file_section in file_contents.split("\n\n\n"):
        print("-------------------------------------------")
        for question_section in file_section.split("\n\n"):
            print(question_section)
            print("______________________________________")


if __name__ == "__main__":
    main()
