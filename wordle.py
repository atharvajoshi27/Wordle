import random
import nltk
import sys

nltk.download('words')

doc = """
INSTRUCTIONS:
1. Writing the result
    if output is "GREEN GREEN YELLOW BLACK YELLOW"
    then result should be written as "ygyby"
2. If word is not found in the word list
    write "none" in the result
3. Everything is case insensitive
"""

class Wordle():
    def __init__(self):
        self.words = list(set(map(lambda x: x.upper(), filter(lambda x: len(x)==5, nltk.corpus.words.words()))))
        self.round = 0
        self.allowed = set()

    # print(len(words))
    def won(self, result):
        return result.lower() == "ggggg"

    def get_unique(self):
        # print(f"len(words) = {len(words)}")
        if(len(self.words) == 0):
            return False
        for i in range(min(100, len(self.words))): # try max 100 times
            word = random.choice(self.words)
            if len(set(word)) == 5:
                return word
        return random.choice(self.words)

    def check_must_dict(self, word):
        for key in self.must_dict.keys():
            letter = key
            for pos in self.must_dict[key]:
                if word[pos] != letter:
                    return False
        return True

    def check_cannot_dict(self, word):
        for key in self.cannot_dict.keys():
            letter = key
            for pos in self.cannot_dict[key]:
                if word[pos] == letter:
                    return False
        return True

    def check_not_allowed(self, word):
        for letter in self.not_allowed:
            if letter in word:
                return False
        return True

    def check_must(self, word):
        for letter in self.must:
            if not letter in word:
                return False
        return True

    
    def solve(self):
        print(doc)
        while self.round < 6:
            self.must = set()
            self.not_allowed = set()
            self.must_dict = dict()
            self.cannot_dict = dict()

            word = self.get_unique()
            if word is False:
                print("Some result has been entered incorrectly.")
                sys.exit(1)
            print(f"Round {self.round+1}: {word}")
            result = input('Result : ').lower()
            if(result == "none"):
                self.words.remove(word)
                continue

            if self.won(result):
                print("Bingo! You won!")
                sys.exit(0)

            for i in range(len(result)):
                letter = word[i]
                color = result[i].upper()
                pos = i

                if color == 'G':
                    self.must.add(letter)
                    self.allowed.add(letter)
                    self.must_dict[letter] = self.must_dict.get(letter, set())
                    self.must_dict[letter].add(pos)
                
                elif color == 'B':
                    if letter in self.allowed:
                        self.cannot_dict[letter] = self.cannot_dict.get(letter, set())
                        self.cannot_dict[letter].add(pos)
                    else:
                        self.not_allowed.add(letter)
                
                elif color == 'Y':
                    self.must.add(letter)
                    self.allowed.add(letter)
                    self.cannot_dict[letter] = self.cannot_dict.get(letter, set())
                    self.cannot_dict[letter].add(pos)
                
                else:
                    print("Wrong result posted.")
                    sys.exit(1)

            filtered_words = []
            for word in self.words:
                if self.check_must_dict(word) and self.check_cannot_dict(word) and self.check_not_allowed(word) and self.check_must(word):
                    filtered_words.append(word)
            self.words = filtered_words
            self.round += 1

        print("Alas! We lost.")


if __name__ == "__main__":
    w = Wordle()
    w.solve()