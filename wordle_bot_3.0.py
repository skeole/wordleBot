import json
from tqdm import tqdm as tqdm

with open("wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers

with open("wordle_accepted_guesses.json") as fileInput:
    ListOfGuesses = json.load(fileInput) #accepted guesses

with open("Bot3BestGuesses.json") as fileInput:
    ApprovedGuesses = json.load(fileInput)

with open("Bot3GrayAnswers.json") as fileInput:
    NextApprovedGuesses = json.load(fileInput)

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

lastword = input("what word do you want to start with (recommended: \"raise\"): ")

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
    else:
        if (lastword in ApprovedGuesses) and (len(Yellow) + len(Green) == 0):
            temp = NextApprovedGuesses[ApprovedGuesses.index(lastword)]
        else:
            temp = findOptimizedWord(ListOfGuesses, ListOfWords)

        print("best word to guess: " + temp[0] + " (Nash Equilbrium: " + str(temp[1]) + " words remaining after guess)")
        if (input("do you want to see all possible answers? y/n: ") == "y"):
            print(ListOfWords)
        lastword = input("what word will you guess: ")

        run = (input("continue? (y for yes, anything else for no): ") == "y")