import os
import sys
import statistics
import time
from collections import defaultdict
from typing import Callable

from wordle.game import LetterStates, WORD_LENGTH, ALPHABET, get_result


def set_print(enabled: bool) -> None:
    if enabled:
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, 'w')


def compute_letter_frequencies(dictionary: list[str]) -> dict[str, float]:
    word_count = len(dictionary)
    letter_counts = defaultdict(lambda: 0)

    for word in dictionary:
        for letter in word:
            letter_counts[letter] += 1

    letter_counts = dict(sorted(letter_counts.items(), key=lambda item: item[1], reverse=True))
    letter_frequencies = {letter: count / (word_count * WORD_LENGTH) for [letter, count] in letter_counts.items()}

    return letter_frequencies


def compute_word_scores(dictionary: list[str], letter_frequencies: dict[str, float]):
    # Compute score based on sum of unique letter probabilities
    word_scores = defaultdict(lambda: 0)
    for word in dictionary:
        word_score = 0
        for letter in set(word):
            word_score += letter_frequencies[letter]

        word_scores[word] = word_score

    word_scores = sorted(word_scores.items(), key=lambda item: item[1], reverse=True)

    return word_scores


def get_guess(dictionary: list[str]) -> str:
    letter_frequencies = compute_letter_frequencies(dictionary)
    print("Letter frequencies")
    for [letter, frequency] in letter_frequencies.items():
        print(f"\t{letter}: {frequency * 100:.2f}%")

    word_scores = compute_word_scores(dictionary, letter_frequencies)
    print("Top guesses")
    for i in range(min(len(word_scores), 5)):
        print(f"\t{word_scores[i]}")

    return word_scores[0][0]


def update_dictionary(dictionary: list[str], guess: str, result: str) -> list[str]:
    possible_letters = [{letter: True for letter in ALPHABET} for _ in range(WORD_LENGTH)]
    must_contain = set()
    present_letters = defaultdict(lambda: False)
    correct_letters = defaultdict(lambda: {"correct": False, "positions": []})
    for i, (letter, state) in enumerate(zip(guess, result)):
        if state == LetterStates.ABSENT:
            continue

        if state == LetterStates.PRESENT:
            possible_letters[i].pop(letter, None)
            present_letters[letter] = True
        elif state == LetterStates.CORRECT:
            possible_letters[i] = {letter: True}
            correct_letters[letter]["correct"] = True
            correct_letters[letter]["positions"].append(i)

        must_contain.add(letter)

    # Absent is more complicated than you think
    for i, (letter, state) in enumerate(zip(guess, result)):
        if state == LetterStates.ABSENT:
            # Yellow and black (whether or not with green), not where the black is
            if present_letters[letter]:
                possible_letters[i].pop(letter, None)
            # Green and black, not anywhere in word except where the green is
            elif correct_letters[letter]["correct"]:
                for j in range(len(possible_letters)):
                    if j not in correct_letters[letter]["positions"]:
                        possible_letters[j].pop(letter, None)
            # Just a black, not anywhere in word
            else:
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


def solve(dictionary: list[str], result_getter: Callable[[str], str] = None) -> int:
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

        dictionary = update_dictionary(dictionary, guesses[-1], results[-1])

    print(f"\r\nYou won in {len(guesses)} guesses")
    for guess in guesses:
        print(f"\t{guess}")

    return len(guesses)


def evaluate(dictionary: list[str]) -> None:
    print(f"Evaluating {len(dictionary)} words")

    attempts = []
    start = time.time()
    for i, target_word in enumerate(dictionary):
        print(f"{i + 1} / {len(dictionary)}")
        set_print(False)
        attempts.append(solve(dictionary.copy(), result_getter=lambda guess: get_result(target_word, guess)))
        set_print(True)
    end = time.time()
    print(f"Evaluation took {(end - start):.2f} seconds")

    success_rate = len([attempt for attempt in attempts if attempt <= 6]) / len(attempts) * 100
    avg = statistics.mean(attempts)
    median = statistics.median(attempts)
    max_guesses = max(attempts)

    set_print(False)
    first_guess = get_guess(dictionary)
    set_print(True)

    print(f"Success rate: {success_rate:.2f}%")
    print(f"Average guesses: {avg:.2f}")
    print(f"Median guesses: {median}")
    print(f"Max guesses: {max_guesses}")
    print(f"First guess: {first_guess}")

    print(f"|[sha](url)|{success_rate:.2f}%|{avg:.2f}|{median:.0f}|{max_guesses}|{first_guess}|")
