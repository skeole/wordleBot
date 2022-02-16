#not copied from 3b1b
import json
import math
import random
from tqdm import tqdm as tqdm

with open("../Word_Data/wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers

with open("../Word_Data/wordle_accepted_guesses.json") as fileInput:
    ListOfGuesses = json.load(fileInput) #accepted guesses

for i in ListOfWords:
    ListOfGuesses.append(i)

ListOfTernaryOptions = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                for m in range(3):
                    temp = [[], [], []]
                    temp[i].append(1)
                    temp[j].append(2)
                    temp[k].append(3)
                    temp[l].append(4)
                    temp[m].append(5)
                    ListOfTernaryOptions.append(temp)

def getRandomElements(List, NumberOfElements):
    list = []
    for i in range(NumberOfElements):
        list.append(random.choice(List))
    return list

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

def expectedInformationGiven(word, answers):
    expectations = 0.0
    for i in ListOfTernaryOptions:
        temp = len(wordsThatFit(word, answers, i[1], i[2]))
        if temp > 0:
            expectations += (temp/len(answers)) * math.log((len(answers)/temp), 2) #2nd part = # of bits
        #1st #: probability that the word is here
            #we want to weight more if the length is less
    return expectations

def findBest(options, answers):
    max = 0.0
    best = ""
    for i in tqdm(options):
        temp = expectedInformationGiven(i, answers)
        if temp > max:
            max = temp
            best = i
    return best

def expected_2_deep_information(word, options, answers):
    expectations = 0.0
    for i in ListOfTernaryOptions: #what are the letter guesses
        temp = wordsThatFit(word, answers, i[1], i[2]) #words remaining
        if len(temp) > 0:
            expectations += (len(temp) / len(answers)) * math.log((len(answers) / len(temp)), 2)  # 2nd part = # of bits
            expectations += (len(temp) / len(answers)) * expectedInformationGiven(findBest(options, temp), temp)
        # 1st #: probability that the word is here
        # we want to weight more if the length is less
    return expectations

print(expectedInformationGiven("soare", ListOfWords))
print(expected_2_deep_information("soare", ListOfWords, ListOfGuesses))
print(findBest(ListOfGuesses, ListOfWords))