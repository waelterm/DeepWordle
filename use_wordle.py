from data_preprocessor import load_dictionary
from wordle_solver import GreedyWordleSolver
import numpy as np


if __name__ == '__main__':
    solution = [None, None, None, None, None]
    state = np.array([1] * (6 * 26))
    solved = False
    cnt = 0
    dictionary = load_dictionary('data/words_alpha.txt')
    my_solver = GreedyWordleSolver(dictionary)
    while not solved:
        guess = my_solver.make_a_guess(solution, state)
        print(f"Guess: {guess}")
        feedback = input("Feedback: (- nothing, e exists, c correct): ")
        while feedback == "na" or feedback == "NA":
            guess = my_solver.make_a_guess(solution, state)
            print(f"Guess: {guess}")
            feedback = input("Feedback: (- nothing, e exists, c correct): ")
        correct_values = 0
        for i in range(5):
            letter = guess[i]
            if feedback[i] == 'c':
                solution[i] = letter
                state[i * 26:(i + 1) * 26] = 0
                state[i * 26 + my_solver.letters_to_idx[letter]] = 1
                solution[i] = letter
                correct_values += 1
                if correct_values == 5:
                    solved = True
                    print("Congratulations!!!")
                    break
            elif feedback[i] == 'e':
                state[i * 26 + my_solver.letters_to_idx[letter]] = 0
                state[5 * 26 + my_solver.letters_to_idx[letter]] = 0
            elif feedback[i] == "-":
                state[0 * 26 + my_solver.letters_to_idx[letter]] = 0
                state[1 * 26 + my_solver.letters_to_idx[letter]] = 0
                state[2 * 26 + my_solver.letters_to_idx[letter]] = 0
                state[3 * 26 + my_solver.letters_to_idx[letter]] = 0
                state[4 * 26 + my_solver.letters_to_idx[letter]] = 0