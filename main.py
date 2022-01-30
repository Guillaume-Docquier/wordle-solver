from dictionaries import Languages, dictionaries
from solver.solver import solve

LANGUAGE_LIST = [language.value for language in Languages]
WORD_LENGTH = 5


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


if __name__ == "__main__":
    while True:
        language = pick_language()
        solve(dictionaries[language].copy())
        print("")
