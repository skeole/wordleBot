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

def draw_centered_rectangle(x_center, y_center, width, height, color, surface=gameDisplay, fill=0, border_radius=0):
    #fill: 0 if fully filled, >1 for line thickness
    pygame.draw.rect(surface, color, [int(x_center - (width/2)), int(y_center - (height/2)), int(width), int(height)], width=int(fill), border_radius=int(border_radius))

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
        for event in pygame.event.get(): #basically go over every event
                        #this includes, but is not limited to: change in mouse position,
                        #     mouse down/up, keys down/up (and which specific key), etc.
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
            print(event)

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