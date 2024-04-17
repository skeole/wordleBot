import json # best word: roate apparently?
from tqdm import tqdm as tqdm
import math

with open("Word_Data/wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers

with open("Word_Data/wordle_accepted_guesses.json") as fileInput:
    ListOfGuesses = json.load(fileInput) #accepted guesses

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
    for i in range(len(dividedAnswers)):
        dividedAnswers[i] = []
    for i in ListOfRemainingAnswers:
        dividedAnswers[decodeYellowGreen(findYellowGreen(Word, i)[0], findYellowGreen(Word, i)[1])].append(i)
    return dividedAnswers

def findNashEquilibrium(ListOfAllGuesses, ListOfRemainingAnswers, primary_weight):
    primary_score = 1000000000
    bestWords = []
    #plan: go over all starting words
    for i in tqdm(ListOfAllGuesses): #I think this is necessary
        temp = divideUpAnswers(ListOfRemainingAnswers, i)
        temp_score_1 = primary_weight(temp)
        if (temp_score_1 < primary_score):
            primary_score = temp_score_1
            bestWords = [i]
        elif (temp_score_1 == primary_score):
            bestWords.append(i)
    if len(bestWords) > 20:
        for i in range(len(bestWords) - 1, -1, -1):
            if bestWords[i] not in ListOfRemainingAnswers:
                bestWords.pop(i)
    return [bestWords, abs(primary_score)]
  
def decodeYellowGreen(yellows, greens):
    s = 0
    for i in range(1, 6):
        if i in yellows:
            s += 3**(i-1)
        if i in greens:
            s += 2 * (3**(i-1))
    return s
    
#functions go here

def total_sum_of_lengths(L):
    s = 0
    for i in L:
        s += len(i)
    return s

def maximum(list_of_numbers): #remember, less is better
    temp = 0
    for i in list_of_numbers:
        temp = max(temp, len(i)) #note this is equivalent to maximum ln, log2, etc.
    return temp

def information(list_of_numbers):
    temp = 0
    for i in list_of_numbers:
        if len(i) > 0: #Make it return negative if you want highest score instead
            temp -= float(len(i))/total_sum_of_lengths(list_of_numbers)*math.log2(float(total_sum_of_lengths(list_of_numbers))/len(i))
    return temp

def possible_answer(list_of_numbers):
    return 1 - len(list_of_numbers[242])

def squared_sum(list_of_numbers):
    temp = 0
    for i in list_of_numbers:
        temp += len(i)*len(i)
    return temp

primary = squared_sum

lastword = input("what's your first guess: ")
print("starting word: \"" + lastword + "\"")

run = True
while run:

    Yellow = []
    Green = []
    temp = input("What positions were yellow: ").split()
    for i in temp:
        Yellow.append(int(i))
    temp = input("What positions were green: ").split()
    for i in temp:
        Green.append(int(i))

    ListOfWords = wordsThatFit(lastword, ListOfWords, Yellow, Green)

    if len(ListOfWords) == 1:
        print("the word is " + ListOfWords[0])
        run = False
    elif len(ListOfWords) == 2:
        print("there are 2 remaining words: \"" + ListOfWords[0] + "\" and \"" + ListOfWords[1] + "\". ")
        run = False
    else:
        if input("do you want to find the best remaining word? ") == "y":
            temp = findNashEquilibrium(ListOfGuesses, ListOfWords, primary)
            print("Best word: \"" + str(temp[0]) + "\". Score: " + str(temp[1]) +
                ". There are " + str(len(ListOfWords)) + " words left currently. ")
            if (len(ListOfWords) < 10):
                print("They are: " + str(ListOfWords))
        else:
            print("There are " + str(len(ListOfWords)) + " words left currently. ")
        lastword = input("What will you guess? ")
    if run:
        run = (input("continue? (y for yes, anything else for no): ") == "y")
        print()