import random
import time
import g4f
import os


def load_words_from_file(filename="russian_words.txt"):
    """Загружает слова и категории из файла"""
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден! Создайте файл со словами.")
        return None

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

    # Проверяем, что файл не пустой
    if not categories:
        print(f"Файл {filename} пуст или содержит только категории без слов!")
        return None

    return categories


def get_hint(word, category, guessed_letters):
    """Функция получения подсказки с обработкой ошибок"""
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{
                'role': 'system',
                'content': f"Дай подсказку для слова '{word}' (категория: {category}) в игре 'Виселица', не называя само слово. Уже угаданы буквы: {', '.join(guessed_letters)}. Ответь 1-2 предложениями на русском."
            }],
            timeout=15
        )
        return response if response else f"Слово связано с: {category}"
    except Exception as e:
        # Альтернативная подсказка если нейросеть недоступна
        hidden_letters = [c for c in word if c not in guessed_letters]
        sample = random.sample(hidden_letters, min(3, len(hidden_letters)))
        return f"Категория: {category}. Попробуйте буквы: {', '.join(sample)}"


def draw_hangman(attempts_left):
    """Рисуем виселицу в зависимости от попыток"""
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


def select_word(words):
    """Выбираем случайное слово и категорию"""
    category = random.choice(list(words.keys()))
    word = random.choice(words[category])
    return word, category


def play_game(words):
    """Основная функция игры"""
    word, category = select_word(words)
    word = word.lower()
    guessed_letters = []
    attempts = 6
    hint_used = False

    print("\nДобро пожаловать в игру 'Виселица'!")
    print(f"Категория: {category}")
    print(f"Слово состоит из {len(word)} букв")
    draw_hangman(attempts)

    while attempts > 0:
        # Показываем текущее состояние слова
        display = [letter if letter in guessed_letters else "_" for letter in word]
        print("\nСлово:", " ".join(display))

        # Проверяем победу
        if all(letter in guessed_letters for letter in word):
            print(f"\nПоздравляем! Вы угадали слово: {word.upper()}!")
            return True

        # Меню выбора действия
        print("\n1 - Угадать букву")
        print("2 - Получить подсказку")
        choice = input("Выберите действие (1/2): ").strip()

        if choice == "1":
            # Обработка угадывания буквы
            guess = input("Введите букву: ").lower().strip()

            if len(guess) != 1 or not guess.isalpha():
                print("Пожалуйста, введите одну букву!")
                continue

            if guess in guessed_letters:
                print("Вы уже называли эту букву!")
                continue

            guessed_letters.append(guess)

            if guess not in word:
                attempts -= 1
                print(f"\nНет такой буквы! Осталось попыток: {attempts}")
                draw_hangman(attempts)
                if attempts == 0:
                    print(f"\nИгра окончена! Загаданное слово: {word.upper()}")
                    return False
            else:
                print("\nВерно! Эта буква есть в слове.")

        elif choice == "2":
            # Обработка запроса подсказки
            if not hint_used:
                print("\nГенерация подсказки...")
                hint = get_hint(word, category, guessed_letters)
                print(f"\nПодсказка: {hint}")
                hint_used = True
                time.sleep(2)  # Пауза для чтения подсказки
            else:
                print("\nВы уже использовали подсказку!")
        else:
            print("\nНекорректный выбор!")


if __name__ == "__main__":
    print("Игра 'Виселица' с подсказками от нейросети")
    print("----------------------------------------")

    # Загружаем слова из файла
    words = load_words_from_file()
    if not words:
        print("Не удалось загрузить слова для игры.")
        exit()

    while True:
        result = play_game(words)

        if result:
            print("Вы победили! 🎉")
        else:
            print("Попробуйте ещё раз! 💪")

        again = input("\nХотите сыграть ещё? (да/нет): ").lower()
        if again not in ["да", "д", "yes", "y"]:
            print("\nСпасибо за игру! До свидания!")
            break