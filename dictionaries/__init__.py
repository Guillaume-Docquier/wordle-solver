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
    Languages.SPANISH.value: spanish_words,
}
