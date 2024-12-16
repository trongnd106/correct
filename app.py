import random
import re

import numpy as np

NUM_OF_TESTS = 1000
dictionary = {}


def addToDictionary(word):
    '''
    # Add word to dictionary.
    # In order to improve performance we assume that there is no typo in first letter
    # Dictionary is map which key is first letter of word and value is array of words which first letter equals to key
    :param word: word which will be added to dictionary
    '''

    if (word[0] in dictionary):
        dictionary[word[0]].append(word)
    else:
        dictionary[word[0]] = [word]


def loadDictionary(path):
    '''

    :param path: path to the file where dictionary is stored
    '''
    f = open(path)

    for line in f:
        addToDictionary(line[:-1].lower())


def findPosition(c):
    '''
    # Find position of character on keyboard
    :param c: Character
    :return: tuple (row,column)
    '''
    row = 0
    column = 0
    keyboard = \
        ["qwertyuiop",
         "asdfghjkl",
         " zxcvbnm"]
    for rownum in range(0, len(keyboard)):

        if c in keyboard[rownum]:
            row = rownum
            column = keyboard[row].find(c)

    return row, column


def distanceOnKeyboard(c1, c2):
    '''
    L1 distance on keyboard
    :param c1: First character
    :param c2: Seconds character
    :return: L1 distance
    '''
    x1, y1 = findPosition(c1)
    x2, y2 = findPosition(c2)
    return abs(x1 - x2) + abs(y1 - y2)


def keyboardDistance(c1, c2):
    '''
    # Function returns distance between characters on keyboard
    :param c1: First character
    :param c2: Second character
    :return: return 0 if characters are equal. Return 1 if sum of their absolute distance is less than 2.
    # Return 2 otherwise
    '''
    if c1 == c2:
        return 0

    if distanceOnKeyboard(c1, c2) <= 2:
        return 1
    else:
        return 2


def defaultLetterDistance(c1, c2):
    '''
    Distance of two characters
    :param c1: First character
    :param c2: Seconds character
    :return: return 0 of they are equal. return 2 otherwise
    '''
    if c1 == c2:
        return 0
    else:
        return 2


def editDistance(s1, s2, ld):
    '''
    # Distance between two strings
    :param s1: First string
    :param s2: Seconds String
    :param ld: Function that calculates distance between two characters
    :return: return edit distance Levenshtein with considering function of letters distance
    '''
    mat = np.zeros((len(s1) + 1, len(s2) + 1))
    for i in range(1, len(s1) + 1):
        mat[i][0] = i
    for j in range(1, len(s2) + 1):
        mat[0][j] = j
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            mat[i][j] = min(mat[i - 1][j - 1] + ld(s1[i - 1], s2[j - 1]), mat[i - 1][j] + 2,
                            mat[i][j - 1] + 2)

    return mat[len(s1)][len(s2)]


def findNearestWords(word, ld):
    '''
    # Search nearest words in dictionary considering function of letter distance
    :param word: word to correct
    :param ld: Function that calculates distance between two characters
    :return: nearest words
    '''
    ans = "Error"
    val = 10

    for w in dictionary[word[0]]:
        dist = editDistance(w, word, ld)
        if dist == val:
            ans = w
        if dist < val:
            ans = w
            val = dist

    return ans


def swapLetter(c):
    '''
    :param c: character
    :return: random character with probability proportional to 1/(distance to c character)
    '''
    letters = "qwertyuiopasdfghjklzxcvbnm"
    probabilities = []
    for l in letters:
        if l == c:
            probabilities.append(0)
            continue
        probabilities.append(random.random() / distanceOnKeyboard(l, c))

    return letters[np.argmax(probabilities)]


def add_error(word):
    '''
    swap with probability 0.25 character in word using swapLetter function
    :param word: string
    :return: string with swapped characters
    '''

    one_letter_chance = 0.25
    for i in range(1, len(word)):
        if random.random() < one_letter_chance:
            word = word[:i] + swapLetter(word[i]) + word[i + 1:]

    return word


def test(path):
    '''
    Compare two method default Levenshtein method and Levenshtein method that considering keyboard layout
    :param path: path to file to test
    '''
    random.seed(1)
    test = []
    file = open(path)
    lines = []
    for line in file:
        lines.append(line)

    for i in range(0, len(lines)):
        test.append((lines[i][:-1].lower(), add_error(lines[i][:-1].lower())))

    right_corrected_k = 0
    right_corrected = 0
    for i in range(NUM_OF_TESTS):
        ind = random.randint(0, len(test))
        print(i, " - Test number ", test[ind][1], " -> ", test[ind][0])
        corrected_k = findNearestWords(test[ind][1], keyboardDistance)
        corrected = findNearestWords(test[ind][1], defaultLetterDistance)
        if corrected_k == test[ind][0]:
            right_corrected_k += 1
        if corrected == test[ind][0]:
            right_corrected += 1

    print(right_corrected, "Number of tests that passed using default Levinstein distance")
    print(right_corrected_k, "Number of tests that passed using Levinstein distance considering keyboard layout")


loadDictionary("dataset.txt")
test("dataset.txt")

