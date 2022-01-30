from collections import defaultdict
from dictionaries import Languages, dictionaries

LANGUAGE_LIST = [language.value for language in Languages]
WORD_LENGTH = 5

ABSENT = 0
PRESENT = 1
CORRECT = 2


def pick_language() -> str:
    print("Choose language:")
    for i, language in enumerate(LANGUAGE_LIST):
        print(f"\t [{i}] {language}")

    language_index = len(LANGUAGE_LIST)
    while language_index < 0 or language_index >= len(LANGUAGE_LIST):
        print("You choice: ", end='')
        language_index = int(input())

    language = LANGUAGE_LIST[language_index]
    print(f"You chose: {language}")

    return language


def get_guess(dictionary):
    # Compute letter frequencies
    word_count = len(dictionary)
    letter_counts = defaultdict(lambda: 0)

    for word in dictionary:
        for letter in word:
            letter_counts[letter] += 1

    print("Letter frequencies")
    letter_counts = dict(sorted(letter_counts.items(), key=lambda item: item[1], reverse=True))
    letter_frequencies = {letter: count / (word_count * WORD_LENGTH) for [letter, count] in letter_counts.items()}
    for [letter, frequency] in letter_frequencies.items():
        print(f"\t{letter}: {frequency * 100:.2f}%")

    # Compute score based on sum of unique letter probabilities
    word_scores = defaultdict(lambda: 0)
    for word in dictionary:
        word_score = 0
        for letter in set(word):
            word_score += letter_frequencies[letter]

        word_scores[word] = word_score

    # Return top guess
    word_scores = sorted(word_scores.items(), key=lambda item: item[1], reverse=True)
    print("Top guesses")
    for i in range(min(len(word_scores), 5)):
        print(f"\t{word_scores[i]}")

    return word_scores[0][0]


def update_dictionary(dictionary, guesses, results):
    possible_letters = defaultdict(lambda: list("qwertyuiopasdfghjklzxcvbnm\xf1"))
    must_contain = []
    for guess, result in zip(guesses, results):
        if guess in dictionary:
            dictionary.remove(guess)

        for i, (letter, res) in enumerate(zip(guess, result)):
            if res == ABSENT:
                for j in range(WORD_LENGTH):
                    if letter in possible_letters[j]:
                        possible_letters[j].remove(letter)
            elif res == PRESENT:
                if letter in possible_letters[i]:
                    possible_letters[i].remove(letter)
                must_contain.append(letter)
            elif res == CORRECT:
                possible_letters[i] = [letter]

    new_dictionary = []
    for word in dictionary:
        valid_word = True
        for letter in must_contain:
            if letter not in word:
                valid_word = False

        for i, letter in enumerate(word):
            if word[i] not in possible_letters[i]:
                valid_word = False

        if valid_word:
            new_dictionary.append(word)

    print(f"New dictionary contains {len(new_dictionary)} words")

    return new_dictionary


def solve_wordle(dictionary):
    print(f"Dictionary contains {len(dictionary)} words")

    results = []
    guesses = []
    while len(results) == 0 or not all(res == 2 for res in results[-1]):
        guess = get_guess(dictionary)
        guesses.append(guess)
        print(f"\r\nGuess: {guess}")

        print(f"[{ABSENT}]: Absent, [{PRESENT}]: Present, [{CORRECT}]: Correct")
        print("Input result: ", end="")
        results.append([int(res) for res in input()])

        dictionary = update_dictionary(dictionary, guesses, results)

    print(f"\r\nYou won in {len(guesses)} guesses")
    for guess in guesses:
        print(f"\t{guess}")


if __name__ == "__main__":
    while True:
        language = pick_language()
        solve_wordle(dictionaries[language].copy())
        print("")
