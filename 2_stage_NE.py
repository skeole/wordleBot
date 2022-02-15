import json
from tqdm import tqdm as tqdm

with open("wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers

with open("wordle_accepted_guesses.json") as fileInput:
    ListOfLGuesses = json.load(fileInput) #accepted guesses

for i in ListOfWords:
    ListOfLGuesses.append(i)

ListOfGuesses = ["soare", "roate", "raise", "raile", "reast", "slate", "crate", "salet", "irate", "trace", "arise", "orate", "stare", "carte", "raine", "slane", "carle", "roast", "torse", "carse", "toile", "trone", "crane", "slant", "trice", "least", "slart"]

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
        print(i, temp, temp3)
    return bestWord, min, min2

def findDoubleNashEquilib(word, ListOfAllWords, LOAG): #find worst case then nash on that
    temp = 0
    temp4 = []
    for j in ListOfAllWords: #go over all words
        temp2 = findYellowGreen(word, j)
        yellow = temp2[0]
        green = temp2[1]
        c = wordsThatFit(word, ListOfAllWords, yellow, green)
        if len(c) > temp:
            temp = len(c) #nash equilib
            temp4 = c #worse case ListOfAllWords
        #temp4: worst case
    return findOptimizedWord(LOAG, temp4)


#print(findOptimizedWord(ListOfGuesses, ListOfWords))

findOptimizedWord(ListOfGuesses, ListOfWords)
#best: raise, with 168 for nash equilibrium