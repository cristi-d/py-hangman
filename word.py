from typing import List


class Word:
    HIDDEN_LETTER = "_"

    def __init__(self, word):
        self._word = word
        self._revealed = list(Word.HIDDEN_LETTER * len(word))
        self._revealed_count = 0

    def reveal(self, letter) -> (bool, List[str]):
        did_match = False
        for i, word_letter in enumerate(self._word):
            if letter.lower() == word_letter.lower():
                # If it's a new letter
                if self._revealed[i] == Word.HIDDEN_LETTER:
                    self._revealed_count += 1
                    did_match = True

                self._revealed[i] = letter

        return did_match, self._revealed

    @property
    def word(self):
        return self._word

    @property
    def is_complete(self):
        return self._revealed_count == len(self._word)

    @property
    def revealed(self):
        return self._revealed
