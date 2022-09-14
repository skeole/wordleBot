import json
from tqdm import tqdm as tqdm

import sys
sys.path.insert(1, '/Users/shaankeole/Downloads/Coding/wordleBot')

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

def findScore(word, ListOfAllWords, greenweight, yellowweight):
    score = 0
    for i in ListOfAllWords:
        t = []
        for j in range(5):
            if word[j] == i[j]: #if the letter matches up exactly - i.e. green
                score += (greenweight-yellowweight)
            if (word[j] in i) and (word[j] not in t): #don't want to double count :)
                t.append(word[j])
                score += yellowweight
    return (score/len(ListOfAllWords))

def findBestWord(ListOfAllGuesses, ListOfAllWords, greenweight, yellowweight):
    maxScore = 0.0
    bestWord = ""
    bestWord2 = ""
    for i in tqdm(ListOfAllGuesses):
        if findScore(i, ListOfAllWords, greenweight, yellowweight) > maxScore:
            maxScore = findScore(i, ListOfAllWords, greenweight, yellowweight)
            bestWord = i
    maxScore = 0.0
    for i in ListOfAllWords:
        if findScore(i, ListOfAllWords, greenweight, yellowweight) > maxScore:
            maxScore = findScore(i, ListOfAllWords, greenweight, yellowweight)
            bestWord2 = i
    return [bestWord, bestWord2]

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
    for i in tqdm(ListOfAllGuesses): #go over every possible guess
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

g = int(input("how much do you want to weigh greens (recommended 2): "))
y = int(input("how much do you want to weigh yellows (recommended 1): "))
if y == 0:
    lastword = ["saree", 0]
elif g/y == 2:
    lastword = ["soare", 0]
elif g/y == 1:
    lastword = ["oater", 0]
elif g/y == 0:
    lastword = ["estro", 0]
else:
    lastword = findBestWord(ListOfGuesses, ListOfWords, g, y)
lastword = input("what word do you want to start with (recommended: \"" + lastword[0] + "\" or \"raise\"): ")

run = True
while run:

    Gray = []
    Yellow = []
    Green = []
    temp = input("What positions were yellow: ").split()
    for i in temp:
        Yellow.append(int(i))
    temp = input("What positions were green: ").split()
    for i in temp:
        Green.append(int(i))
    for i in range(1, 6):
        if (i not in Green) and (i not in Yellow):
            Gray.append(int(i))

    ListOfWords = wordsThatFit(lastword, ListOfWords, Yellow, Green)

    temp = findBestWord(ListOfGuesses, ListOfWords, g, y)

    bestguessableword = temp[0]
    bestanswerableword = temp[1]
    print("best word to guess is: " + bestguessableword)
    print("best answerable word is: " + bestanswerableword)
    if (input("do you want to see all possible answers? y/n: ") == "y"):
        print(ListOfWords)
    if (input("do you want ur computer to die? y/n: ") == "y"):
        print(findOptimizedWord(ListOfGuesses, ListOfWords))
    lastword = input("what word will you guess: ")

    run = (input("continue? (y for yes, anything else for no): ") == "y")