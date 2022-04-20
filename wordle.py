from data_preprocessor import load_dictionary
import random
import numpy as np

random.seed(33)

class Wordle:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        #self.start_new_game()
        self.solved = False
        self.state = np.array([1]*(6*26))
        self.letters_to_idx, self.idx_to_letter = self.build_letter_index_dicts()

    def build_letter_index_dicts(self):
        letters_to_idx = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9,
                          "k":10, "l":11, "m":12, "n":13, "o":14, "p":15, "q":16, "r":17, "s":18, "t":19, "u":20, "v":21, "w":22, "x":23, "y":24, "z":25}
        idx_to_letter = {}
        for key,value in letters_to_idx.items():
            idx_to_letter[value] = key
        return letters_to_idx, idx_to_letter


    def start_new_game(self):
        word_id = random.randint(0,len(self.dictionary))
        self.word = self.dictionary[word_id]
        self.solution = [None, None, None, None, None]
        self.solved = False
        print(f"Word to be found: {self.word}")
        return self.solution, self.solved, self.state

    def process_input(self, guess):
        if guess == self.word:
            self.solved = True
        if len(guess)!= 5:
            print("Invalid Input")
            return None
        else:
            for pos,letter in enumerate(guess):
                if letter == self.word[pos]:
                    self.solution[pos] = letter
                    self.state[pos*26:(pos+1)*26] = 0
                    self.state[pos * 26 + self.letters_to_idx[letter]] = 1
                elif letter in self.word:
                    self.state[pos * 26 + self.letters_to_idx[letter]] = 0
                    self.state[5 * 26 + self.letters_to_idx[letter]] = 0
                else:
                    self.state[0 * 26 + self.letters_to_idx[letter]] = 0
                    self.state[1 * 26 + self.letters_to_idx[letter]] = 0
                    self.state[2 * 26 + self.letters_to_idx[letter]] = 0
                    self.state[3 * 26 + self.letters_to_idx[letter]] = 0
                    self.state[4 * 26 + self.letters_to_idx[letter]] = 0
        return self.solution, self.solved, self.state


if __name__ == '__main__':
    dictionary = load_dictionary('data/words_alpha.txt')
    my_wordle = Wordle(dictionary)
    for i in range(6):
        guess = input("Make a guess: ")
        my_wordle.process_input(guess)