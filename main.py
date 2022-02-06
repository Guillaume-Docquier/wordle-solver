from enum import Enum

from dictionaries import Languages, dictionaries
from solver.solver import evaluate, solve


class Modes(Enum):
    PLAY = "play"
    EVAL = "eval"


MODE_LIST = [mode.value for mode in Modes]
LANGUAGE_LIST = [language.value for language in Languages]


def pick(label, value_list):
    print(f"Choose {label}:")
    for i, value in enumerate(value_list):
        print(f"\t [{i}] {value}")

    value_index = len(value_list)
    while value_index < 0 or value_index >= len(value_list):
        print("Your choice: ", end='')
        value_index = int(input())

    value = value_list[value_index]
    print(f"You chose: {value}\r\n")

    return value


if __name__ == "__main__":
    while True:
        mode = pick("mode", MODE_LIST)
        language = pick("language", LANGUAGE_LIST)
        dictionary = dictionaries[language].copy()

        if mode == Modes.PLAY.value:
            print(dictionary[3467 - 1])
            solve(dictionary)
        elif mode == Modes.EVAL.value:
            evaluate(dictionary)

        print("")
