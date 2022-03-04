guess = "crate" #THIS IS WHAT YOU NEED TO CHANGE

import json
from tqdm import tqdm as tqdm

with open("Word_Data/wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers

with open("Word_Data/wordle_accepted_guesses.json") as fileInput:
    ListOfGuesses = json.load(fileInput) #accepted guesses

for i in ListOfWords:
    ListOfGuesses.append(i)

def decode(code): #code = 0 to 242
    GYG = [[], [], []]
    GYG[int(code/1) % 3].append(1)
    GYG[int(code/3) % 3].append(2)
    GYG[int(code/9) % 3].append(3)
    GYG[int(code/27) % 3].append(4)
    GYG[int(code/81) % 3].append(5)
    return GYG

def encode(yellows, greens):
    s = 0
    for i in range(1, 6):
        if i in yellows:
            s += 3**(i-1)
        if i in greens:
            s += 2 * (3**(i-1))
    return s

def find_yellows_and_greens(guess, target):
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

def words_that_fit(word, answers, yellows, greens):
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

def separate_answers_by_yellows_and_greens(ListOfRemainingAnswers, Word):
    dividedAnswers = [0]*243
    for i in ListOfRemainingAnswers:
        dividedAnswers[encode(find_yellows_and_greens(Word, i)[0], find_yellows_and_greens(Word, i)[1])] += 1
    return dividedAnswers

def find_nash_equilbrium(ListOfAllGuesses, ListOfRemainingAnswers):
    minimum = 10000
    minimum2 = 10000000
    bestWord = ""
    #plan: go over all starting words
    for i in ListOfAllGuesses: #I think this is necessary
        maximum = 0 #go over the 243 possible groups, see the size of each one
        temp = 0
        for j in separate_answers_by_yellows_and_greens(ListOfRemainingAnswers, i): #go over all possible green/yellow combos, then take which one gives the nash equilib
            maximum = max(maximum, j)
            temp += j*j
        if (maximum < minimum) or ((maximum == minimum) and (temp <= minimum2)):
            minimum = maximum
            bestWord = i
    return [bestWord, minimum]

def required_number_of_guesses(target, ListOfGuesses, ListOfWords):
    lastword = guess
    run = True
    numGuesses = 1.0
    if target == guess:
        return 1.0
    LOW = ListOfWords
    while run:
        numGuesses += 1
        temp0 = find_yellows_and_greens(lastword, target)
        if lastword != guess:
            LOW = words_that_fit(lastword, LOW, temp0[0], temp0[1])
        else:
            LOW = dividedList[encode(temp0[0], temp0[1])]

        if len(LOW) == 1:
            run = False
        elif len(LOW) == 2:
            numGuesses += 0.5
            run = False
        elif lastword == guess:
            lastword = ListOfNextGuesses[encode(temp0[0], temp0[1])]
        else:
            lastword = find_nash_equilbrium(ListOfGuesses, LOW)[0]
        if numGuesses > 10:
            run = False
    return numGuesses
            
ListOfNextGuesses = []

with open("Starting_Word.txt", "w") as outFile:
    outFile.write(guess + "\n")
    for i in tqdm(range(0, 243)):
        temp2 = decode(i)
        temp = words_that_fit(guess, ListOfWords, temp2[1], temp2[2])
        if len(temp) > 2:
            temp2 = find_nash_equilbrium(ListOfGuesses, temp)
            outFile.write(str(temp2[0]) + " " + str(temp2[1]) +  "\n")
            ListOfNextGuesses.append(temp2[0])
        else:
            outFile.write(str(temp) + "\n")
            ListOfNextGuesses.append(0)

total_number_of_guesses = 0.0
ListOfFailures = []
ListOfSixes = []
ListOfFives = []

dividedList = separate_answers_by_yellows_and_greens(ListOfWords, guess)
for i in tqdm(ListOfWords):
    t = required_number_of_guesses(i, ListOfGuesses, ListOfWords)
    total_number_of_guesses += t

    if t > 6:
        ListOfFailures.append(i)
    elif t > 5:
        ListOfSixes.append(i)
    elif t > 4:
        ListOfFives.append(i)

print("There are " + str(len(ListOfFailures)) + " words that fail: " + str(ListOfFailures))
print("There are " + str(len(ListOfSixes)) + " words that take 6 guesses: " + str(ListOfSixes))
print("There are " + str(len(ListOfFives)) + " words that take 5 guesses: " + str(ListOfFives))
print("Average Number Of Guesses: " + str(total_number_of_guesses / len(ListOfWords)))
print("Total Number Of Guesses: " + str(int(total_number_of_guesses)))