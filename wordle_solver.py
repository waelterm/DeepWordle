from data_preprocessor import load_dictionary
from wordle import Wordle
import random

class GreedyWordleSolver:

    def __init__(self, dictionary):
        self.original_dictionary = dictionary
        self.filtered_dictionary = dictionary
        self.word = ""
        self.letters_to_idx, self.idx_to_letter = self.build_letter_index_dicts()


    def build_letter_index_dicts(self):
        letters_to_idx = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
                          "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19,
                          "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}
        idx_to_letter = {}
        for key, value in letters_to_idx.items():
            idx_to_letter[value] = key
        return letters_to_idx, idx_to_letter

    def skip_word(self):
        print(f"filtered dict: {self.filtered_dictionary}")
        print(f"Word: {self.word}")
        self.filtered_dictionary.remove(self.word)

    def filter_solutions(self, state):
        new_dictionary = []
        #print(f"L2I: {self.letters_to_idx}")
        for word in self.filtered_dictionary:
            consider_word = True
            for pos, letter in enumerate(word):
                if state[pos*26 + self.letters_to_idx[letter]] == 0:
                    consider_word = False
            for letter_idx in range(26):
                if state[5*26 + letter_idx] == 0 and self.idx_to_letter[letter_idx] not in word:
                    consider_word = False
            if consider_word:
                new_dictionary.append(word)
        self.filtered_dictionary = new_dictionary

    def calculate_probabilities(self, solution):
        letter_probabilities_dict = {}
        for word in self.filtered_dictionary:
            for pos, letter in enumerate(word):
                if solution[pos] is None:
                    if letter in letter_probabilities_dict.keys():
                        letter_probabilities_dict[letter] += 1
                    else:
                        letter_probabilities_dict[letter] = 1
        return letter_probabilities_dict

    def calculate_word_scores(self, letter_probability_dict):
        scores = []
        for word in self.filtered_dictionary:
            score = 1
            letters = []
            for letter in word:
                if letter in letter_probability_dict.keys() and letter not in letters:
                    score *= letter_probability_dict[letter]
                letters.append(letter)
            scores.append(score)
        return scores

    def pick_best_guess(self, scores):
        guess_idx = scores.index(max(scores))
        guess = self.filtered_dictionary[guess_idx]
        self.word = guess
        return guess


    def make_a_guess(self, solution, state):
        self.filter_solutions(state)
        letter_probability_dict = self.calculate_probabilities(solution)
        scores = self.calculate_word_scores(letter_probability_dict)
        guess = self.pick_best_guess(scores)
        self.filtered_dictionary.remove(guess)
        return guess

class RandomWordleSolver:

    def __init__(self, dictionary):
        self.original_dictionary = dictionary

    def skip_word(self):
        print(f"filtered dict: {self.filtered_dictionary}")
        print(f"Word: {self.word}")

    def make_a_guess(self, solution, state):
        guess_id = random.randint(0,len(self.original_dictionary)-1)
        guess = self.original_dictionary[guess_id]
        return guess

class FilterWordleSolver:

    def __init__(self, dictionary):
        self.original_dictionary = dictionary
        self.filtered_dictionary = dictionary
        self.letters_to_idx, self.idx_to_letter = self.build_letter_index_dicts()

    def build_letter_index_dicts(self):
        letters_to_idx = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
                          "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19,
                          "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}
        idx_to_letter = {}
        for key, value in letters_to_idx.items():
            idx_to_letter[value] = key
        return letters_to_idx, idx_to_letter

    def skip_word(self):
        print(f"filtered dict: {self.filtered_dictionary}")
        print(f"Word: {self.word}")

    def filter_solutions(self, state):
        new_dictionary = []
        #print(f"L2I: {self.letters_to_idx}")
        for word in self.filtered_dictionary:
            consider_word = True
            for pos, letter in enumerate(word):
                if state[pos*26 + self.letters_to_idx[letter]] == 0:
                    consider_word = False
            for letter_idx in range(26):
                if state[5*26 + letter_idx] == 0 and self.idx_to_letter[letter_idx] not in word:
                    consider_word = False
            if consider_word:
                new_dictionary.append(word)
        self.filtered_dictionary = new_dictionary

    def make_a_guess(self, solution, state):
        self.filter_solutions(state)
        guess_id = random.randint(0,len(self.filtered_dictionary)-1)
        guess = self.filtered_dictionary[guess_id]
        return guess




if __name__ == '__main__':
    dictionary = load_dictionary('data/words_alpha.txt')
    cnts =0
    num_of_tests = 1000
    guesses_needed = 0
    for i in range(num_of_tests):
        my_wordle = Wordle(dictionary)
        my_solver = FilterWordleSolver(dictionary)
        solution, solved, state = my_wordle.start_new_game()
        cnt = 0
        while not solved:
            #print(f"state: {state}")
            guess = my_solver.make_a_guess(solution, state)
            print(f"  Guess: {guess}")
            solution, solved, state = my_wordle.process_input(guess)
            cnt += 1
            guesses_needed += 1
        if cnt <= 6:
            cnts += 1
    print(f"Solved {cnts} out of {num_of_tests} in 6 tries or less.")
    print(f"Success Rate: {cnts/num_of_tests * 100}%")
    print(f"Average number of trials: {guesses_needed/num_of_tests}")