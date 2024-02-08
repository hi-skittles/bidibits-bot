import csv
from secrets import choice
from typing import List


class Wordle:
    def __init__(self, where_are_my_words: str = "words.csv", tries: int = 0, max_tries: int = 6) -> None:
        self.where_are_my_words = where_are_my_words
        self.words = self.load_words()
        self.retrieve_word = self.get_word()
        self.tries = tries
        self.max_tries = max_tries

    def load_words(self) -> List[str]:
        words = []
        with open(self.where_are_my_words, "r", newline="") as wordscsv:
            reader = csv.reader(wordscsv)
            next(reader)
            for row in reader:
                words.append(row[0])
        return words

    def get_word(self) -> str:
        return choice(self.words)