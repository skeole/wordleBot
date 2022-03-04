import json
from tqdm import tqdm as tqdm

with open("Word_Data/wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers

with open("Word_Data/wordle_accepted_guesses.json") as fileInput:
    ListOfGuesses = json.load(fileInput) #accepted guesses

for i in ListOfWords:
    ListOfGuesses.append(i)

def findYellowGreen1(code): #code = 0 to 242
    GYG = [[], [], []]
    GYG[int(code/1) % 3].append(1)
    GYG[int(code/3) % 3].append(2)
    GYG[int(code/9) % 3].append(3)
    GYG[int(code/27) % 3].append(4)
    GYG[int(code/81) % 3].append(5)
    return GYG

def decodeYellowGreen(yellows, greens):
    s = 0
    for i in range(1, 6):
        if i in yellows:
            s += 3**(i-1)
        if i in greens:
            s += 2 * (3**(i-1))
    return s

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

def wordsThatFit(word, answers, yellows, greens):
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

def numOfWordsThatFit(word, answers, yellows, greens): #grays, greens, yellows = positions
    grays = []
    for i in range(1, 6):
        if (i not in yellows) and (i not in greens):
            grays.append(i)
    k = 0
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
            k += 1 #wordsthatfit.append(i)
    return k #wordsthatfit

def findOptimizedWord(ListOfAllGuesses, ListOfAllWords):
    min = 10000
    min2 = 10000
    bestWord = ""
    for i in tqdm(ListOfAllGuesses): #go over every possible guess
        temp = 0
        temp3 = 0
        for j in ListOfAllWords: #go over all the remaining words
            temp2 = findYellowGreen(i, j)
            yellow = temp2[0]
            green = temp2[1]
            c = numOfWordsThatFit(i, ListOfAllWords, yellow, green)
            temp = max(temp, c) #nash equilib
            temp3 += c * c
        if ((temp == min) and (temp3 < min2)) or (temp < min):
            min = temp
            min2 = temp3
            bestWord = i
    return bestWord, min, min2

def WordsInThisScenario(ListOfRemainingAnswers, Word, yellows, greens):
    AnswersThatFit = 0
    for i in ListOfRemainingAnswers:
        if findYellowGreen(i, Word) == [yellows, greens]:
            AnswersThatFit += 1
    return AnswersThatFit

def divideUpAnswers(ListOfRemainingAnswers, Word):
    dividedAnswers = [0]*243
    for i in ListOfRemainingAnswers:
        dividedAnswers[decodeYellowGreen(findYellowGreen(Word, i)[0], findYellowGreen(Word, i)[1])] += 1
    return dividedAnswers

def optimizedFindOptimizedWord(ListOfAllGuesses, ListOfRemainingAnswers):
    minimum = 10000
    minimum2 = 10000000
    bestWord = ""
    #plan: go over all starting words
    for i in ListOfAllGuesses: #I think this is necessary
        maximum = 0 #go over the 243 possible groups, see the size of each one
        temp = 0
        for j in divideUpAnswers(ListOfRemainingAnswers, i): #go over all possible green/yellow combos, then take which one gives the nash equilib
            maximum = max(maximum, j)
            temp += j*j
        if (maximum < minimum) or ((maximum == minimum) and (temp <= minimum2)):
            minimum = maximum
            bestWord = i
    return [bestWord, minimum]
            

guess = "qajaq" #THIS IS WHAT YOU NEED TO CHANGE

with open("Starting_Word.txt", "w") as outFile:
    outFile.write(guess + "\n")
    for i in tqdm(range(0, 243)):
        temp2 = findYellowGreen1(i)
        temp = wordsThatFit(guess, ListOfWords, temp2[1], temp2[2])
        if len(temp) > 2:
            temp2 = optimizedFindOptimizedWord(ListOfGuesses, temp)
            outFile.write(str(temp2[0]) + " " + str(temp2[1]) +  "\n")
        else:
            outFile.write(str(temp) + "\n")