import pygame
import math

class New_Object(object):
    ListOfPoints = []
    hitbox = []
    x = 0
    y = 0
    angle = 0
    def __init__(self, ListOfPoints, ListOfColors, surface, border_width=0): #should be a nested list
                            #ex. [[(2, 3), (4, 5)], [(6, 7), (8, 9)]] -> 2 objects with points
                            #2, 3 and 4, 5 for object 1 and 6, 7 and 8, 9 for object 2
        self.ListOfPoints = ListOfPoints
        self.ListOfColors = ListOfColors
        self.surface = surface
        self.border_width = border_width
        
    def rotateTo(self, angle):
        self.angle = (-1) * angle * math.pi/180.0
    
    def update_hitbox(self):
        self.hitbox = []
        for i in self.ListOfPoints: #for every shape in ListOfPoints
            polygon = []
            for j in i:
                point = (self.x+j[0]*math.cos(self.angle)-j[1]*math.sin(self.angle), 
                         self.y+j[0]*math.sin(self.angle)+j[1]*math.cos(self.angle))
                polygon.append(point) #in form [(x1, y1), (x2, y2), ...]
            self.hitbox.append(polygon)
    
    def draw(self):
        self.update_hitbox()
        for i in range(len(self.hitbox)): #for every shape in the hitbox
            pygame.draw.polygon(self.surface, self.ListOfColors[i], self.hitbox[i], width=self.border_width)

def point_above_line(point, line): #definition of "above": y above line, or if vertical, then x value greater
    #point format: (x, y)
    #line format: [(x1, y1), (x2, y2)]
    if line[0][0] == line[1][0]:
        return point[0] > line[0][0]
    elif point[0] == line[0][0]:
        return point[1] > line[0][1]
    elif point[0] > line[0][0]:
        return (point[1]-line[0][1])/(point[0]-line[0][0]) > (line[1][1]-line[0][1])/(line[1][0]-line[0][0])
    else:
        return (point[1]-line[0][1])/(point[0]-line[0][0]) < (line[1][1]-line[0][1])/(line[1][0]-line[0][0])

def point_on_line(point, line):
    if abs(line[1][0]-line[0][0]) == 0:
        return abs(line[0][0] - point[0]) < 0.01
    elif abs(point[0]-line[0][0]) == 0:
        return False
    else:
        return (point[1]-line[0][1])/(point[0]-line[0][0]) == (line[1][1]-line[0][1])/(line[1][0]-line[0][0])

def intersect(line_1, line_2):
    if (max(line_1[0][0], line_1[1][0]) < min(line_2[0][0], line_2[1][0])) or (min(line_1[0][0], line_1[1][0]) > max(line_2[0][0], line_2[1][0])) or (max(line_1[0][1], line_1[1][1]) < min(line_2[0][1], line_2[1][1])) or (min(line_1[0][1], line_1[1][1]) > max(line_2[0][1], line_2[1][1])):
        return False #legit zero chance they intersect
    
    temp_1 = line_1[1][0]
    temp_2 = line_2[1][0]
    if line_1[0][0] == line_1[1][0]:
        temp_1 += 0.01
    if line_2[0][0] == line_2[1][0]:
        temp_2 += 0.01
    lein_1 = [line_1[0], (temp_1, line_1[1][1])]
    lein_2 = [line_2[0], (temp_2, line_2[1][1])]
    
    if point_on_line(lein_1[0], lein_2) or point_on_line(lein_1[1], lein_2) or point_on_line(lein_2[0], lein_1) or point_on_line(lein_2[1], lein_1):
        return False #if any of the points are on the line
    else:
        return (point_above_line(lein_1[0], lein_2) != point_above_line(lein_1[1], lein_2)) and (point_above_line(lein_2[0], lein_1) != point_above_line(lein_2[1], lein_1))

def point_inside_polygon(point, polygon, accuracy=6): #we want the inside-ness to be the same for every line
    #solution - very scuffed - kinda LOLLY - but should work
    min_x = 10000000
    min_y = 10000000
    max_x = -10000000
    max_y = -10000000
    for i in polygon:
        min_x = min(min_x, i[0])
        max_x = max(max_x, i[0])
        min_y = min(min_y, i[1])
        max_y = max(max_y, i[1])
    length = math.sqrt((max_x-min_x)*(max_x-min_x)+(max_y-min_y)*(max_y-min_y))
    
    for i in range(accuracy): #go over "accuracy" radial lines
        temp = 0
        
        for j in range(len(polygon)): #add 1 if intersects line, 0.5 for each endpoint it touches
            radial_line = [point, (point[0] + length*math.cos(2*math.pi/accuracy * i), point[1] + length*math.sin(2*math.pi/accuracy * i))]
            if point_on_line(polygon[j], radial_line):
                temp += 1
            if point_on_line(polygon[(j+1) % len(polygon)], radial_line):
                temp += 1
            if intersect(radial_line, 
                         [polygon[j], polygon[(j+1) % len(polygon)]]):
                temp += 2
            #see if the radial line intersects any of the hitbox lines
        
        if temp % 4 != 2:
            return False
    return True

finalWord = input("Final Word: ")
n = int(input("number of guesses: "))
guesses = ["      "] * 6
for i in range(n):
    guesses[i] = input("next guess: ")

def text_objects(text, font, color):
    textSurface = font.render(text, True, color) #what the thing renders as
            #(xpos, ypos, xlength, ylength) <------|; default x, y is 0, 0; ylength = font size
    return textSurface, textSurface.get_rect() # .get_rect() is the rectangle

def display_message(text, font_size, x_position, y_position, color, surface):
    largeText = pygame.font.SysFont("arial-bold", int(font_size)) #what font and font size
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (int(x_position), int(y_position))
    surface.blit(TextSurf, TextRect) #prepare to add
    
class button(New_Object):
    letter = "";
    def __init__(self, point, color, letter, surface):
        self.letter = letter;
        super().__init__([[(-40, -40), (-40, 40), (40, 40), (40, -40)]], [color], surface)
        self.x = point[0]
        self.y = point[1]
    
    def draw2(self):
        self.draw()
        display_message(self.letter, 70, self.x, self.y + 5, (255, 255, 255), self.surface)


pygame.init()

display_width = 800.0
display_height = display_width*3/4

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("The NYT ******* Sucks")

clock = pygame.time.Clock()

boxList = []
for i in range(6):
    for j in range(5):
        boxList.append(button((50 + j * 87, 50 + i * 88), (58, 58, 60), guesses[i][j].upper(), gameDisplay))

def game_loop():
    run = True
    
    while run:

        for event in pygame.event.get(): #basically go over every event
                        #this includes, but is not limited to: change in mouse position,
                        #     mouse down/up, keys down/up (and which specific key), etc.
            if event.type == pygame.QUIT:
                run = False
        #print(mouse_x, mouse_y)
        #print(ListOfButtons)
        gameDisplay.fill((18, 18, 19));
        for object in boxList:
            object.draw2()
        
        pygame.display.update() #the graphics all refresh
        clock.tick(20) #20 FPS


game_loop()
pygame.quit()
quit()
