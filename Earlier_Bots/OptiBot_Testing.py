import json
from tqdm import tqdm as tqdm

with open("Word_Data/wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers

with open("Word_Data/wordle_accepted_guesses.json") as fileInput:
    ListOfGuesses = json.load(fileInput) #accepted guesses

ListOfNextGuesses = []

with open("Starting_Word.txt") as fileInput:
    file = list(fileInput)

firstguess = ""

for line in file:
    C = line.strip()
    C = C.split()
    if firstguess == "":
        firstguess = C[0]
    else:
        ListOfNextGuesses.append(C[0])

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

def divideUpAnswers(ListOfRemainingAnswers, Word):
    dividedAnswers = [0]*243
    for i in ListOfRemainingAnswers:
        dividedAnswers[decodeYellowGreen(findYellowGreen(Word, i)[0], findYellowGreen(Word, i)[1])] += 1
    return dividedAnswers

def divideList(ListOfRemainingAnswers, Word):
    dividedAnswers = [0]*243
    for i in range(len(dividedAnswers)):
        dividedAnswers[i] = []
    for i in ListOfRemainingAnswers:
        dividedAnswers[decodeYellowGreen(findYellowGreen(Word, i)[0], findYellowGreen(Word, i)[1])].append(i)
    return dividedAnswers

def findOptimizedWord(ListOfAllGuesses, ListOfRemainingAnswers):
    minimum = 10000
    bestWord = ""
    #plan: go over all starting words
    for i in ListOfAllGuesses: #I think this is necessary
        maximum = 0 #go over the 243 possible groups, see the size of each one
        for j in divideUpAnswers(ListOfRemainingAnswers, i): #go over all possible green/yellow combos, then take which one gives the nash equilib
            maximum = max(maximum, j)
        if (maximum < minimum) or ((maximum == minimum) and (i in ListOfRemainingAnswers)):
            minimum = maximum
            bestWord = i
    return [bestWord, minimum]

def decodeYellowGreen(yellows, greens):
    s = 0
    for i in range(1, 6):
        if i in yellows:
            s += 3**(i-1)
        if i in greens:
            s += 2 * (3**(i-1))
    return s

def findNumGuesses(target, ListOfGuesses, ListOfWords):
    lastword = firstguess
    run = True
    numGuesses = 1.0
    if target == firstguess:
        return 1.0
    LOW = ListOfWords
    while run:
        numGuesses += 1
        temp0 = findYellowGreen(lastword, target)
        if lastword != firstguess:
            LOW = wordsThatFit(lastword, LOW, temp0[0], temp0[1])
        else:
            LOW = dividedList[decodeYellowGreen(temp0[0], temp0[1])]

        if len(LOW) == 1:
            run = False
        elif len(LOW) == 2:
            numGuesses += 0.5
            run = False
        elif lastword == firstguess:
            lastword = ListOfNextGuesses[decodeYellowGreen(temp0[0], temp0[1])]
        else:
            lastword = findOptimizedWord(ListOfGuesses, LOW)[0]
        if numGuesses > 10:
            run = False
    return numGuesses

s = 0.0
ListOfFailures = []
ListOfSixes = []
ListOfFives = []

print(firstguess)

dividedList = divideList(ListOfWords, firstguess)
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
'''
raise:
    average amount of guesses: 3.585313174946004
    number of words that require 4.5 or 5 guesses: 114
    number of words that require more than 5: none
    average amount of time spent per word: <1 second

salet:
    average amount of guesses: 3.5399568034557234
    number of words that require 4.5 or 5 guesses: 82
    number of words that require more than 5: None
    average amount of time spent per word: <1 second

adieu:
    average amount of guesses: 3.7293736501079913
    number of words that require 4.5 or 5 guesses: 212
    number of words that require more than 5: none
    average amount of time spent per word: 1 to 2 seconds

crate:
    average amount of guesses: 3.53304535637149
    number of words that require 4.5 or 5 guesses: 92
    number of words that require more than 5: none
    average amount of time spent per word: <1 second

words to try that have the same letters: trace, slate, arise, least
that don't: slane, crane, slant, oater/orate, carte, reast/tears/stare/tares/rates, carle, carte, torse

for fun: qajaq, jazzy, xylyl, pzazz, slyly, susus, yukky, mamma, jaffa
'''