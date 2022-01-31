from enum import Enum
from .english import english_words
from .french import french_words
from .spanish import spanish_words


class Languages(Enum):
    ENGLISH = "english"
    FRENCH = "french"
    SPANISH = "spanish"


dictionaries = {
    Languages.ENGLISH.value: english_words,
    Languages.FRENCH.value: french_words,

    # 92 words contain 5 characters and end with '-'. I don't know what this is.
    Languages.SPANISH.value: [word for word in spanish_words if "-" not in word],
}
