import random


def load_words_with_categories(filename="russian_words.txt"):
    """Загружает слова и категории из файла"""
    categories = {}
    current_category = "Без категории"

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                current_category = line[1:].strip()
                categories[current_category] = []
            else:
                categories.setdefault(current_category, []).append(line.lower())

    # Преобразуем в список кортежей (слово, категория)
    words_with_categories = []
    for category, words in categories.items():
        for word in words:
            words_with_categories.append((word, category))

    return words_with_categories


def draw_hangman(attempts_left):
    """Рисует виселицу в зависимости от оставшихся попыток"""
    stages = [
                """
           ------
           |    |
           |    
           |    
           |    
           |
        --------
        """,

        """
           ------
           |    |
           |    O
           |    
           |    
           |
        --------
        """,

        """
           ------
           |    |
           |    O
           |    |
           |    
           |
        --------
        """,

        """
           ------
           |    |
           |    O
           |   /|
           |    
           |
        --------
        """,

        """
           ------
           |    |
           |    O
           |   /|\\
           |    
           |
        --------
        """,

        """
           ------
           |    |
           |    O
           |   /|\\
           |   / 
           |
        --------
        """,

        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        --------
        
        """

    ]
    print(stages[6 - attempts_left])


def hangman():
    words = load_words_with_categories()
    if not words:
        print("Ошибка: файл со словами не найден или пуст!")
        return

    word, category = random.choice(words)
    guessed_letters = []
    attempts = 6

    print("Добро пожаловать в игру 'Виселица'!")
    print(f"Категория: {category}")
    print(f"Слово состоит из {len(word)} букв.")
    draw_hangman(attempts)  # Начальное состояние виселицы

    while attempts > 0:
        display_word = ""
        for letter in word:
            if letter in guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        print(f"\nСлово: {display_word}")

        if all(letter in guessed_letters for letter in word):
            print("\nПоздравляю! Вы угадали слово!")
            print(f"Это действительно было слово: {word.upper()}")
            break

        guess = input("Введите букву: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Пожалуйста, введите одну русскую букву.")
            continue

        if guess in guessed_letters:
            print("Вы уже называли эту букву.")
            continue

        guessed_letters.append(guess)

        if guess not in word:
            attempts -= 1
            print(f"\nНет такой буквы! Осталось попыток: {attempts}")
            draw_hangman(attempts)
            if attempts == 0:
                print("\nИгра окончена! Вы проиграли.")
                print(f"Загаданное слово было: {word.upper()}")
        else:
            print("\nВерно! Эта буква есть в слове.")


if __name__ == "__main__":
    hangman()