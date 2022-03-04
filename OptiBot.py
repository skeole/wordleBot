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
        ListOfNextGuesses.append(C[1])

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
        dividedAnswers[decodeYellowGreen(findYellowGreen(Word, i)[0], findYellowGreen(Word, i)[1])].append(i) #+= 1
    return dividedAnswers

def findNashEquilibrium(ListOfAllGuesses, ListOfRemainingAnswers):
    minimum = 10000
    bestWord = ""
    #plan: go over all starting words
    for i in tqdm(ListOfAllGuesses): #I think this is necessary
        maximum = 0 #go over the 243 possible groups, see the size of each one
        for j in divideUpAnswers(ListOfRemainingAnswers, i): #go over all possible green/yellow combos, then take which one gives the nash equilib
            maximum = max(maximum, len(j))
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

lastword = firstguess
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
    elif lastword == firstguess:
        print("next word: \"" + ListOfNextGuesses[decodeYellowGreen(Yellow, Green)] +
              "\". Nash Equilbrium: " + ListOfNextGuesses[decodeYellowGreen(Yellow, Green)] +
              " words. There are " + str(len(ListOfWords)) + " words left currently. ")
        lastword = ListOfNextGuesses[decodeYellowGreen(Yellow, Green)]
    else:
        temp = findNashEquilibrium(ListOfGuesses, ListOfWords)
        lastword = temp[0]
        print("next word: \"" + lastword + "\". Nash Equilbrium: " + str(temp[1]) +
              " words. There are " + str(len(ListOfWords)) + " words left currently. ")
    if run:
        run = (input("continue? (y for yes, anything else for no): ") == "y")