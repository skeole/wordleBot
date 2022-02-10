with open("wordle_accepted_words.txt") as fileInput:
    ListOfWords = list(fileInput)
for i in range(len(ListOfWords)):
    ListOfWords[i] = ListOfWords[i].strip()

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

def findBestWord(ListOfAllWords, greenweight, yellowweight):
    maxScore = 0.0
    bestWord = ""
    for i in ListOfAllWords:
        if findScore(i, ListOfAllWords, greenweight, yellowweight) > maxScore:
            maxScore = findScore(i, ListOfAllWords, greenweight, yellowweight)
            bestWord = i
    return(bestWord)

Gray = []
Yellow = []
Green = []

#print(findBestWord(ListOfWords, 3, 2))
print("stare")

run = True
while run:
    temp = input("What letters were gray: ").split()
    for i in temp:
        Gray.append(i)
    temp = input("What letters were yellow and what positions (ex. \"A 2 D 4\"): ").split()
    for i in temp:
        Yellow.append(i)
    temp = input("What letters were green and what positions (ex. \"A 2 D 4\"): ").split()
    for i in temp:
        Green.append(i)

    print(Gray)
    print(Yellow)
    print(Green)

    temp = []
    for element in Gray:
        if (element not in Yellow) and (element not in Green):
            temp.append(element)
    Gray = temp

    temp2 = []
    for word in ListOfWords:
        temp = True
        for i in range(int(len(Green)/2)):
            if word[int(Green[2*i+1])-1] != Green[2*i]:
                temp = False
        if temp:
            for i in range(int(len(Yellow)/2)):
                if (Yellow[2*i] not in word) or (word[int(Yellow[2*i+1])-1] == Yellow[2*i]):
                    temp = False
        if temp:
            for i in Gray:
                if i in word:
                    temp = False
        if temp:
            temp2.append(word)

    ListOfWords = temp2
    #print(ListOfWords)

    print(findBestWord(ListOfWords, 3, 2))

    run = (input("continue? (y for yes, anything else for no): ") == "y")