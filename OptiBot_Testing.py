import json
from tqdm import tqdm as tqdm

with open("wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers

with open("wordle_accepted_guesses.json") as fileInput:
    ListOfGuesses = json.load(fileInput) #accepted guesses

ListOfNextGuesses = []

with open("cheat.txt") as fileInput:
    file = list(fileInput)

for line in file:
    C = line.strip()
    C = C.split()
    ListOfNextGuesses.append([C[1], C[2]])

for i in ListOfWords:
    ListOfGuesses.append(i)

def wordsThatFit(word, answers, yellows, greens): #grays, greens, yellows = positions
    grays = []
    for i in range(1, 6):
        if (i not in yellows) and (i not in greens):
            grays.append(i)
    wordsthatfit = []
    for i in answers:
        temp = True
        temp2 = list(i)
        for j in greens:
            if temp:
                temp = (word[j-1] == temp2[j-1]) #we need all the greens to match
                temp2[j-1] = 0 #now we remove the letter from the answer for yellows and grays
        for j in yellows:
            if temp:
                temp = (word[j-1] in temp2) and (word[j-1] != temp2[j-1])
                #we need the yellows to be in the word but also in a different position
                if temp:
                    temp2[temp2.index(word[j-1])] = 0 #now we remove the letter
        for j in grays:
            if temp:
                temp = (word[j-1] not in temp2)
        if temp:
            wordsthatfit.append(i)
    return wordsthatfit

def findYellowGreen(guess, target):
    r = list(target)
    Green = []
    Yellow = []
    for i in range(5):
        if guess[i] == r[i]:
            r[i] = 0
            Green.append(i+1)
    for i in range(5):
        if (guess[i] in r) and ((i+1) not in Green):
            r[r.index(guess[i])] = 0
            Yellow.append(i+1)
    return [Yellow, Green]

def findOptimizedWord(ListOfAllGuesses, ListOfAllWords):
    min = 10000
    min2 = 10000
    bestWord = ""
    for i in ListOfAllGuesses: #go over every possible guess
        temp = 0
        temp3 = 0
        for j in ListOfAllWords: #go over all the remaining words
            temp2 = findYellowGreen(i, j)
            yellow = temp2[0]
            green = temp2[1]
            c = len(wordsThatFit(i, ListOfAllWords, yellow, green))
            temp = max(temp, c) #nash equilib
            temp3 += c * c
        if ((temp == min) and (temp3 < min2)) or (temp < min):
            min = temp
            min2 = temp3
            bestWord = i
    return bestWord, min, min2

def decodeYellowGreen(yellows, greens):
    s = 0
    for i in range(1, 6):
        if i in yellows:
            s += 3**(i-1)
        if i in greens:
            s += 2 * (3**(i-1))
    return s

def findNumGuesses(target, ListOfGuesses, ListOfWords):
    lastword = "raise"
    run = True
    numGuesses = 1.0
    if target == "raise":
        return 1.0
    LOW = ListOfWords
    while run:
        numGuesses += 1
        temp0 = findYellowGreen(lastword, target)
        LOW = wordsThatFit(lastword, LOW, temp0[0], temp0[1])

        if len(LOW) == 1:
            run = False
        elif len(LOW) == 2:
            numGuesses += 0.5
            run = False
        elif lastword == "raise":
            lastword = ListOfNextGuesses[decodeYellowGreen(temp0[0], temp0[1])][0]
        else:
            lastword = findOptimizedWord(ListOfGuesses, LOW)[0]
        if numGuesses > 10:
            run = False
    return numGuesses

s = 0.0
ListOfFailures = []
ListOfSixes = []
ListOfFives = []

for i in tqdm(ListOfWords):
    t = findNumGuesses(i, ListOfGuesses, ListOfWords)
    s += t

    if t > 6:
        ListOfFailures.append(i)
    elif t > 5:
        ListOfSixes.append(i)
    elif t > 4:
        ListOfFives.append(i)

print(s)
print(ListOfFailures)
print(len(ListOfFailures))
print(ListOfSixes)
print(len(ListOfSixes))
print(ListOfFives)
print(len(ListOfFives))

s = (s / len(ListOfWords))

print(s)

#average amount of guesses: 3.585313174946004
#number of words that require 4.5 or 5 guesses: 114
#number of words that require more than 5: none
#average amount of time spent per word: 0.5922 seconds