from collections import defaultdict

WORD_LENGTH = 5
ALPHABET = list("qwertyuiopasdfghjklzxcvbnm\xf1")


class LetterStates:
    ABSENT = 0
    PRESENT = 1
    CORRECT = 2


def get_result(target_word, guess):
    available_hints = defaultdict(lambda: 0)
    for letter in target_word:
        available_hints[letter] += 1

    result = [LetterStates.ABSENT for _ in range(len(target_word))]
    for i, letter in enumerate(guess):
        if target_word[i] == letter:
            result[i] = LetterStates.CORRECT
            available_hints[letter] -= 1

    for i, letter in enumerate(guess):
        if result[i] != LetterStates.CORRECT and available_hints[letter] > 0 and letter in target_word:
            result[i] = LetterStates.PRESENT
            available_hints[letter] = 0

    return result
