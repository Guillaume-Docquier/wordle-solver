WORD_LENGTH = 5
ALPHABET = list("qwertyuiopasdfghjklzxcvbnm\xf1")


class LetterStates:
    ABSENT = 0
    PRESENT = 1
    CORRECT = 2


def get_result(target_word, guess):
    result = [LetterStates.ABSENT for _ in range(len(target_word))]
    for i, letter in enumerate(guess):
        if letter in target_word:
            result[i] = LetterStates.PRESENT

        if target_word[i] == letter:
            result[i] = LetterStates.CORRECT

    return result
