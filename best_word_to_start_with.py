import random
from tqdm import tqdm as tqdm

with open("wordle_accepted_words.txt") as fileInput:
    ListOfWords = list(fileInput)
for i in range(len(ListOfWords)):
    ListOfWords[i] = ListOfWords[i].strip()

def findScore(word, ListOfAllWords, greenweight, yellowweight):
    score = 0
    for i in ListOfAllWords:
        t = []
        for j in range(5):
            if word[j] == i[j]:  # if the letter matches up exactly - i.e. green
                score += (greenweight - yellowweight)
            if (word[j] in i) and (word[j] not in t):  # don't want to double count :)
                t.append(word[j])
                score += yellowweight
    return (score / len(ListOfAllWords))

def findBestWord(ListOfAllWords, greenweight, yellowweight):
    maxScore = 0.0
    bestWord = ""
    for i in ListOfAllWords:
        if findScore(i, ListOfAllWords, greenweight, yellowweight) > maxScore:
            maxScore = findScore(i, ListOfAllWords, greenweight, yellowweight)
            bestWord = i
    return (bestWord)

def findGrayYellowGreen(word, endword):
    gray = []
    yellow = []
    green = []
    for i in range(len(word)):
        if word[i] not in endword:
            gray.append(word[i])
        elif (word[i] == endword[i]):
            green.append(word[i])
            green.append(i+1)
        else:
            yellow.append(word[i])
            yellow.append(i+1)
    temp = []
    temp.append(gray)
    temp.append(yellow)
    temp.append(green)
    return temp

def findNumberOfGuesses(startword, endword, LOAW, greenweight, yellowweight):
    word = startword
    numguesses = 1
    if (startword == endword):
        return 1
    Gray = []
    Yellow = []
    Green = []
    ListOfWords = LOAW
    #we start with word
    run = True
    while run:
        numguesses += 1
        temp = findGrayYellowGreen(word, endword)
        for i in temp[0]:
            Gray.append(i)
        for i in temp[1]:
            Yellow.append(i)
        for i in temp[2]:
            Green.append(i)

        temp = []
        for element in Gray:
            if (element not in Yellow) and (element not in Green):
                temp.append(element)
        Gray = temp.copy()

        temp2 = []
        for word in ListOfWords:
            temp = True
            for i in range(int(len(Green) / 2)):
                if word[int(Green[2 * i + 1]) - 1] != Green[2 * i]:
                    temp = False
            if temp:
                for i in range(int(len(Yellow) / 2)):
                    if (Yellow[2 * i] not in word) or (word[int(Yellow[2 * i + 1]) - 1] == Yellow[2 * i]):
                        temp = False
            if temp:
                for i in Gray:
                    if i in word:
                        temp = False
            if temp:
                temp2.append(word)

        ListOfWords = temp2
        # print(ListOfWords)

        word = findBestWord(ListOfWords, greenweight, yellowweight)
        run = (word != endword)
    return numguesses

def getRandomElements(List, NumberOfElements):
    list = []
    for i in range(NumberOfElements):
        list.append(random.choice(List))
    return list

def findAvgNumberOfGuesses(startword, LOAW, g, y):
    ave = 0.0
    for i in tqdm(LOAW): #tqdm(getRandomElements(LOAW, 1000)):
        ave += findNumberOfGuesses(startword, i, LOAW, g, y)
    ave = ave / len(LOAW)
    return ave

def findHowManyItFails(startword, LOAW, g, y, maxguesses):
    print(startword)
    count = 0
    listOfFails = []
    for i in tqdm(LOAW): #tqdm(getRandomElements(LOAW, 1000)):
        if (findNumberOfGuesses(startword, i, LOAW, g, y) > maxguesses):
            count += 1
            listOfFails.append(i)
    print(listOfFails)
    return count

#for 1/0: crane = 3.733, slate = 3.686, saine = 3.770, stare = 3.753
#for 3/1: crane = 3.676, slate = 3.605, saine = 3.703, stare = 3.651
#for 2/1: crane = 3.641, slate = 3.600, saine = 3.701, stare = 3.631
#for 7/4: crane = 3.627, slate = 3.613, saine = 3.698, stare = 3.633
#for 3/2: crane = 3.626, slate = 3.611, saine = 3.690, stare = 3.632
#for 1/1: crane = 3.663, slate = 3.631, saine = 3.710, stare = 3.665

#of times each word fails at 2/1:
    #crane: 13; slate: 11; saine: 18; stare: 16

#special words:
    #soare, 2/1: 3.724 guesses, 21 fails
    #saree, 1/0: 3.957 guesses, 22 fails
    #oater, 1/1: 3.736 guesses, 29 fails

word = "crane"
print(findAvgNumberOfGuesses(word, ListOfWords, 1, 0))