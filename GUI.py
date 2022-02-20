import pygame
import time
import json

ListOfGuesses = []
with open("Word_Data/wordle_accepted_answers.json") as fileInput:
    ListOfWords = json.load(fileInput) #accepted answers
with open("Word_Data/wordle_accepted_guesses.json") as fileInput:
    ListOfGuesses = json.load(fileInput) #accepted guesses
ListOfNextGuesses = []
with open("cheat.txt") as fileInput:
    file = list(fileInput)
first_guess = ""
for line in file:
    C = line.strip()
    C = C.split()
    if first_guess == "":
        first_guess = C[0]
    else:
        ListOfNextGuesses.append([C[1], C[2]])
for i in ListOfWords:
    ListOfGuesses.append(i)

pygame.init()

display_width = 800.0
display_height = display_width*3/4

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Wordle Bot")

#Where is stuff located
#5 word boxes:
#centers are: (170, 400); (285, 400); (400, 400); (515, 400); (630, 400)
#divide by 800, 600 to get in terms of display_width and display_height
#size of boxes: each is 80x80

#RGB Data:
#Table: https://www.rapidtables.com/web/color/RGB_Color.html

black = (0, 0, 0)
white = (234, 234, 234)
gray = (128, 128, 128)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

orange = (255, 128, 0)
yellow = (153, 153, 0)
lime = (76, 153, 0)

clock = pygame.time.Clock()

def text_objects(text, font, color):
    textSurface = font.render(text, True, color) #what the thing renders as
            #(xpos, ypos, xlength, ylength) <------|; default x, y is 0, 0; ylength = font size
    return textSurface, textSurface.get_rect() # .get_rect() is the rectangle

def display_message(text, font_size, x_position, y_position, color, font="futura"):
    font_actual = font
    if font not in ["optima", "georgia", "keyboard", "verdana", "arial", "futura", "comicsans", "gillsans"]:
        font_actual = "futura"
    largeText = pygame.font.SysFont(font_actual, int(font_size)) #what font and font size
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (int(x_position), int(y_position))
    gameDisplay.blit(TextSurf, TextRect) #prepare to add

def color_with_opacity(color, opacity):
    return [color[0], color[1], color[2], opacity]

def draw_centered_rectangle(x_center, y_center, width, height, color, surface=gameDisplay, fill=0, border_radius=0.0):
    #fill: 0 if fully filled, >1 for line thickness
    pygame.draw.rect(surface, color, [int(x_center - (width/2)), int(y_center - (height/2)), int(width), int(height)], width=int(fill), border_radius=int(border_radius))

def button(message, text_color, x, y, width, height, color, surface=gameDisplay, border_radius=0.0, border=0, border_color=black, border_width=0.0, font="futura", font_size=-1):
    if border != 0:
        draw_centered_rectangle(x, y, width+2*border_width, height+2*border_width, border_color, surface=surface, border_radius=border_radius+border_width)
    draw_centered_rectangle(x, y, width, height, color, surface=surface, border_radius=border_radius)
    temp = font_size
    if font_size == -1:
        temp = height * 3 / 4
    display_message(message, temp, x, y, text_color, font=font)

def button_data(message, x, y, width, height):
    return [message, x-width/2, y-height/2, x+width/2, y+height/2]

def words_that_fit(word, answers, yellows, greens): #grays, greens, yellows = positions
    grays = []
    for i in range(1, 6):
        if (i not in yellows) and (i not in greens):
            grays.append(i)
    words_that_fit = []
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
            words_that_fit.append(i)
    return words_that_fit

def find_yellow_green(guess, target):
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

def find_optimized_word(ListOfAllGuesses, ListOfAllWords):
    min = 10000
    min2 = 10000
    bestWord = ""
    for i in ListOfAllGuesses: #go over every possible guess
        temp = 0
        temp3 = 0
        for j in ListOfAllWords: #go over all the remaining words
            temp2 = find_yellow_green(i, j)
            yellow = temp2[0]
            green = temp2[1]
            c = len(words_that_fit(i, ListOfAllWords, yellow, green))
            temp = max(temp, c) #nash equilib
            temp3 += c * c
        if ((temp == min) and (temp3 < min2)) or (temp < min):
            min = temp
            min2 = temp3
            bestWord = i
    return bestWord, min, min2

def decode_yellow_green(yellows, greens):
    s = 0
    for i in range(1, 6):
        if i in yellows:
            s += 3**(i-1)
        if i in greens:
            s += 2 * (3**(i-1))
    return s

def calculate_optimized_word(last_word, yellows, greens, answers):
    if len(answers) == 1:
        return answers[0]
    elif len(answers) == 2:
        return answers[0]# + " " + words_remaining[1]
    elif last_word.lower() == first_guess:
        return ListOfNextGuesses[decode_yellow_green(yellows, greens)][0]
    else:
        return find_optimized_word(ListOfGuesses, answers)[0]

def game_loop():
    run = True

    list_of_words = ListOfWords

    mouse_pressed = False

    mouse_x = 0
    mouse_y = 0

    mouse_ticks = 0
    calculating_on = False

    last_word = first_guess.upper()
    words_remaining = ListOfWords
    chosen_font = "verdana"
        #must be from ["optima", "georgia", "keyboard", "verdana",
    #                   "arial", "futura", "comicsans", "gillsans"]
    list_of_squares = [0, 0, 0, 0, 0]
    list_of_colors = [gray, yellow, lime]
    while run:

        reset = False

        ListOfButtons = []

        mouse_clicked = False
        mouse_released = False

        for event in pygame.event.get(): #basically go over every event
                        #this includes, but is not limited to: change in mouse position,
                        #     mouse down/up, keys down/up (and which specific key), etc.
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
                mouse_pressed = True
                mouse_ticks += 1

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_released = True
                mouse_pressed = False
                mouse_ticks += 1
            #print(event)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print(mouse_x, mouse_y)
        gameDisplay.fill(black) #sets the background to white = (255, 255, 255)

        button("calculate best word", white, 40*display_width/80, 15*display_height/60, 40*display_width/80, 4*display_height/60, black, border_radius=5*display_height/60, border=1, border_color=white, border_width=5*display_width/800, font=chosen_font)
        ListOfButtons.append(button_data("calculate best word", 40*display_width/80, 15*display_height/60, 40*display_width/80, 4*display_height/60))

        button(last_word[0], white, 17*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, list_of_colors[list_of_squares[0]], font=chosen_font)
        ListOfButtons.append(button_data("letter 1", 17*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60))

        button(last_word[1], white, 28.5*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, list_of_colors[list_of_squares[1]], font=chosen_font)
        ListOfButtons.append(button_data("letter 2", 28.5*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60))

        button(last_word[2], white, 40*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, list_of_colors[list_of_squares[2]], font=chosen_font)
        ListOfButtons.append(button_data("letter 3", 40*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60))

        button(last_word[3], white, 51.5*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, list_of_colors[list_of_squares[3]], font=chosen_font)
        ListOfButtons.append(button_data("letter 4", 51.5*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60))

        button(last_word[4], white, 63*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, list_of_colors[list_of_squares[4]], font=chosen_font)
        ListOfButtons.append(button_data("letter 5", 63*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60))

        button("reset", white, 40*display_width/80, 6*display_height/60, 40*display_width/80, 4*display_height/60, black, border_radius=5*display_height/60, border=1, border_color=white, border_width=5*display_width/800, font=chosen_font)
        ListOfButtons.append(button_data("reset", 40*display_width/80, 6*display_height/60, 40*display_width/80, 4*display_height/60))

        #print(mouse_x, mouse_y)
        #print(ListOfButtons)
        if (ListOfButtons[0][1] <= mouse_x) and (mouse_x <= ListOfButtons[0][3]) and (ListOfButtons[0][2] <= mouse_y) and (mouse_y <= ListOfButtons[0][4]):
            if mouse_clicked:
                calculating_on = True
        if mouse_clicked and ((ListOfButtons[1][1] <= mouse_x) and (mouse_x <= ListOfButtons[1][3]) and (ListOfButtons[1][2] <= mouse_y) and (mouse_y <= ListOfButtons[1][4])):
            list_of_squares[0] += 1
            list_of_squares[0] = (list_of_squares[0] % 3)
        if mouse_clicked and ((ListOfButtons[2][1] <= mouse_x) and (mouse_x <= ListOfButtons[2][3]) and (ListOfButtons[2][2] <= mouse_y) and (mouse_y <= ListOfButtons[2][4])):
            list_of_squares[1] += 1
            list_of_squares[1] = (list_of_squares[1] % 3)
        if mouse_clicked and ((ListOfButtons[3][1] <= mouse_x) and (mouse_x <= ListOfButtons[3][3]) and (ListOfButtons[3][2] <= mouse_y) and (mouse_y <= ListOfButtons[3][4])):
            list_of_squares[2] += 1
            list_of_squares[2] = (list_of_squares[2] % 3)
        if mouse_clicked and ((ListOfButtons[4][1] <= mouse_x) and (mouse_x <= ListOfButtons[4][3]) and (ListOfButtons[4][2] <= mouse_y) and (mouse_y <= ListOfButtons[4][4])):
            list_of_squares[3] += 1
            list_of_squares[3] = (list_of_squares[3] % 3)
        if mouse_clicked and ((ListOfButtons[5][1] <= mouse_x) and (mouse_x <= ListOfButtons[5][3]) and (ListOfButtons[5][2] <= mouse_y) and (mouse_y <= ListOfButtons[5][4])):
            list_of_squares[4] += 1
            list_of_squares[4] = (list_of_squares[4] % 3)
        if mouse_clicked and ((ListOfButtons[6][1] <= mouse_x) and (mouse_x <= ListOfButtons[6][3]) and (ListOfButtons[6][2] <= mouse_y) and (mouse_y <= ListOfButtons[6][4])):
            reset = True

        if calculating_on:
            display_message("calculating...", display_height/15, display_width/2, display_height/3, white)

        pygame.display.update() #the graphics all refresh
        clock.tick(20) #20 FPS
        if calculating_on:
            yellows = []
            greens = []
            for i in range(len(list_of_squares)):
                if list_of_squares[i] == 1:
                    yellows.append(i+1)
                elif list_of_squares[i] == 2:
                    greens.append(i+1)
            words_remaining = words_that_fit(last_word.lower(), words_remaining, yellows, greens)
            last_word = calculate_optimized_word(last_word, yellows, greens, words_remaining).upper()
            list_of_squares = [0, 0, 0, 0, 0]
            print(last_word)
            calculating_on = False

        if reset:
            last_word = first_guess.upper()
            words_remaining = ListOfWords
            calculating_on = False
            list_of_squares = [0, 0, 0, 0, 0]




game_loop()
pygame.quit()
quit()

'''
NOTES:
(0, 0) is at the top left corner

#best fonts:
optima
georgia
keyboard
verdana
arial
future
comicsans
gillsans
'''