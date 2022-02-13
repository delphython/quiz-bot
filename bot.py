def main():
    with open("quiz-questions/1vs1200.txt", "r", encoding="koi8-r") as file:
        file_contents = file.read()

    print(file_contents)


if __name__ == "__main__":
    main()
