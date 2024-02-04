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


game = Wordle("words.csv", 0, 6)
word_answer = game.retrieve_word
print(word_answer)

while game.tries < game.max_tries:
    game.tries += 1
    guess = input("Enter a guess: ")
    if len(guess) != 5:
        game.tries -= 1
        continue
    if guess == word_answer:
        print("You win!")
        break
    else:
        for i, j in zip(guess, word_answer):
            if j in guess and j in i:
                print(f"{i}✔")
            elif j in guess:
                print(f"{j}➕")
            else:
                print(f"{i}❌")
else:
    print(f"You lose! The word was {word_answer}.")
