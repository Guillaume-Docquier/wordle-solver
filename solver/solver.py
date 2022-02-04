import os
import sys
from collections import defaultdict
import statistics

from wordle.game import LetterStates, WORD_LENGTH, ALPHABET, get_result


def set_print(enabled):
    if enabled:
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, 'w')


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
    possible_letters = [{letter: True for letter in ALPHABET} for _ in range(WORD_LENGTH)]
    must_contain = set()
    for guess, result in zip(guesses, results):
        if guess in dictionary:
            dictionary.remove(guess)

        letter_was_handled = defaultdict(lambda: False)
        for i, (letter, state) in enumerate(zip(guess, result)):
            if state == LetterStates.ABSENT:
                continue

            if state == LetterStates.PRESENT:
                possible_letters[i].pop(letter, None)
            elif state == LetterStates.CORRECT:
                possible_letters[i] = {letter: True}

            must_contain.add(letter)
            letter_was_handled[letter] = True

        # Absent only means absent if there's no other hints about the letter
        for i, (letter, state) in enumerate(zip(guess, result)):
            if state == LetterStates.ABSENT and not letter_was_handled[letter]:
                for j in range(len(possible_letters)):
                    possible_letters[j].pop(letter, None)

    new_dictionary = []
    for word in dictionary:
        valid_word = True
        for letter in must_contain:
            if letter not in word:
                valid_word = False
                break

        if valid_word:
            for i, letter in enumerate(word):
                if word[i] not in possible_letters[i]:
                    valid_word = False
                    break

        if valid_word:
            new_dictionary.append(word)

    print(f"New dictionary contains {len(new_dictionary)} words")

    return new_dictionary


def solve(dictionary, result_getter=None):
    print(f"Dictionary contains {len(dictionary)} words")

    guesses = []
    results = []
    while len(results) == 0 or not all(res == LetterStates.CORRECT for res in results[-1]):
        guess = get_guess(dictionary)
        guesses.append(guess)
        print(f"\r\nGuess: {guess}")

        print(f"[{LetterStates.ABSENT}]: Absent, [{LetterStates.PRESENT}]: Present, [{LetterStates.CORRECT}]: Correct")
        print("Input result: ", end="")
        if result_getter:
            result = result_getter(guess)
            print(result)
        else:
            result = [int(res) for res in input()]

        results.append(result)

        dictionary = update_dictionary(dictionary, guesses, results)

    print(f"\r\nYou won in {len(guesses)} guesses")
    for guess in guesses:
        print(f"\t{guess}")

    return len(guesses)


def evaluate(dictionary):
    print(f"Evaluating {len(dictionary)} words")

    set_print(False)
    attempts = []
    for i, target_word in enumerate(dictionary):
        attempts.append(solve(dictionary.copy(), result_getter=lambda guess: get_result(target_word, guess)))
    set_print(True)

    success_rate = len([attempt for attempt in attempts if attempt <= 6]) / len(attempts) * 100
    avg = statistics.mean(attempts)
    median = statistics.median(attempts)
    max_guesses = max(attempts)
    first_guess = get_guess(dictionary)

    print(f"Success rate: {success_rate:.2f}%")
    print(f"Average guesses: {avg:.2f}")
    print(f"Median guesses: {median}")
    print(f"Max guesses: {max_guesses}")
    print(f"First guess: {first_guess}")

    print(f"|[sha](url)|{success_rate:.2f}%|{avg:.2f}|{median:.0f}|{max_guesses}|{first_guess}|")
