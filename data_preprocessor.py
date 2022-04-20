import csv


def load_dictionary(filename):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        five_letter_dict = []
        for row in spamreader:
            if len(row[0]) == 5:
                five_letter_dict.append(row[0])
    print(f"Number of five-letter words: {len(five_letter_dict)}")
    return five_letter_dict

if __name__ == '__main__':
    load_dictionary('data/words_alpha.txt')