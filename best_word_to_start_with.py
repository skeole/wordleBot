import random

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

def findNumberOfGuesses(startword, endword, LOAW):
    word = startword
    numguesses = 1
    if (startword == endword):
        return 0
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

        word = findBestWord(ListOfWords, 3, 2)
        run = (word != endword)
    return numguesses

def getRandomElements(List, NumberOfElements):
    list = []
    for i in range(NumberOfElements):
        list.append(random.choice(List))
    return list

def findAvgNumberOfGuesses(startword, LOAW):
    ave = 0.0
    for i in getRandomElements(LOAW, 1000):
        ave += findNumberOfGuesses(startword, i, LOAW)
    ave = ave / 1000
    return ave

word = "stare"
print(word, findAvgNumberOfGuesses(word, ListOfWords))