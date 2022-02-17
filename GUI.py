import pygame
import time

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
white = (255, 255, 255)
gray = (128, 128, 128)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

orange = (255, 128, 0)
yellow = (255, 255, 0)
lime = (128, 255, 0)

clock = pygame.time.Clock()

ListOfButtons = []

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

def game_loop():
    run = True

    mouse_pressed = False

    mouse_x = 0
    mouse_y = 0

    last_word = "RAISE"
    chosen_font = "verdana"
        #must be from ["optima", "georgia", "keyboard", "verdana",
    #                   "arial", "futura", "comicsans", "gillsans"]
    while run:

        ListOfButtons = []

        for event in pygame.event.get(): #basically go over every event
                        #this includes, but is not limited to: change in mouse position,
                        #     mouse down/up, keys down/up (and which specific key), etc.
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
            #print(event)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print(mouse_x, mouse_y)
        gameDisplay.fill(black) #sets the background to white = (255, 255, 255)

        draw_centered_rectangle(17*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, white, border_radius=display_height/80)
        draw_centered_rectangle(28.5*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, white, border_radius=display_height/80)
        draw_centered_rectangle(40*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, white, border_radius=display_height/80)
        draw_centered_rectangle(51.5*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, white, border_radius=display_height/80)
        draw_centered_rectangle(63*display_width/80, 40*display_height/60, 8*display_width/80, 8*display_height/60, white, border_radius=display_height/80)

        display_message(last_word[0], 7*display_width/80, 17*display_width/80, 40*display_height/60, black, font=chosen_font)
        display_message(last_word[1], 7 * display_width / 80, 28.5 * display_width / 80, 40 * display_height / 60, black, font=chosen_font)
        display_message(last_word[2], 7 * display_width / 80, 40 * display_width / 80, 40 * display_height / 60, black, font=chosen_font)
        display_message(last_word[3], 7 * display_width / 80, 51.5 * display_width / 80, 40 * display_height / 60, black, font=chosen_font)
        display_message(last_word[4], 7 * display_width / 80, 63 * display_width / 80, 40 * display_height / 60, black, font=chosen_font)

        button("click here for surprise!", white, 40*display_width/80, 15*display_height/60, 40*display_width/80, 4*display_height/60, black, border_radius=5*display_height/60, border=1, border_color=white, border_width=5*display_width/800, font=chosen_font)
        ListOfButtons.append(button_data("surprise", 40*display_width/80, 15*display_height/60, 40*display_width/80, 4*display_height/60))

        #print(ListOfButtons)
        if mouse_pressed and ((ListOfButtons[0][1] <= mouse_x) and (mouse_x <= ListOfButtons[0][3]) and (ListOfButtons[0][2] <= mouse_y) and (mouse_y <= ListOfButtons[0][4])):
            display_message("calculating...", display_height/15, display_width/2, display_height/3, white)



        if mouse_pressed:
            display_message("Mouse Down", display_height/15, display_width/2, display_height/2, white)
        else:
            display_message("Mouse Up", display_height/15, display_width/2, display_height/2, white)


        pygame.display.update() #the graphics all refresh
        clock.tick(20) #20 FPS


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