from collections import defaultdict

from wordle.game import LetterStates, WORD_LENGTH, ALPHABET


def compute_letter_frequencies(dictionary):
    word_count = len(dictionary)
    letter_counts = defaultdict(lambda: 0)

    for word in dictionary:
        for letter in word:
            letter_counts[letter] += 1

    letter_counts = dict(sorted(letter_counts.items(), key=lambda item: item[1], reverse=True))
    letter_frequencies = {letter: count / (word_count * WORD_LENGTH) for [letter, count] in letter_counts.items()}

    return letter_frequencies


def compute_word_scores(dictionary, letter_frequencies):
    # Compute score based on sum of unique letter probabilities
    word_scores = defaultdict(lambda: 0)
    for word in dictionary:
        word_score = 0
        for letter in set(word):
            word_score += letter_frequencies[letter]

        word_scores[word] = word_score

    word_scores = sorted(word_scores.items(), key=lambda item: item[1], reverse=True)

    return word_scores


def get_guess(dictionary):
    letter_frequencies = compute_letter_frequencies(dictionary)
    print("Letter frequencies")
    for [letter, frequency] in letter_frequencies.items():
        print(f"\t{letter}: {frequency * 100:.2f}%")

    word_scores = compute_word_scores(dictionary, letter_frequencies)
    print("Top guesses")
    for i in range(min(len(word_scores), 5)):
        print(f"\t{word_scores[i]}")

    return word_scores[0][0]


def update_dictionary(dictionary, guesses, results):
    possible_letters = defaultdict(lambda: ALPHABET.copy())
    must_contain = []
    for guess, result in zip(guesses, results):
        if guess in dictionary:
            dictionary.remove(guess)

        for i, (letter, res) in enumerate(zip(guess, result)):
            if res == LetterStates.ABSENT:
                for j in range(WORD_LENGTH):
                    if letter in possible_letters[j]:
                        possible_letters[j].remove(letter)
            elif res == LetterStates.PRESENT:
                if letter in possible_letters[i]:
                    possible_letters[i].remove(letter)
                must_contain.append(letter)
            elif res == LetterStates.CORRECT:
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


def solve(dictionary):
    print(f"Dictionary contains {len(dictionary)} words")

    guesses = []
    results = []
    while len(results) == 0 or not all(res == LetterStates.CORRECT for res in results[-1]):
        guess = get_guess(dictionary)
        guesses.append(guess)
        print(f"\r\nGuess: {guess}")

        print(f"[{LetterStates.ABSENT}]: Absent, [{LetterStates.PRESENT}]: Present, [{LetterStates.CORRECT}]: Correct")
        print("Input result: ", end="")
        results.append([int(res) for res in input()])

        dictionary = update_dictionary(dictionary, guesses, results)

    print(f"\r\nYou won in {len(guesses)} guesses")
    for guess in guesses:
        print(f"\t{guess}")
