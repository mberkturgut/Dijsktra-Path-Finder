from math import sin, cos, pi as PI
import pygame
import random
import sys

count = 100
gridSize = 500
w = h = gridSize

hex_size = 28
epsilon = hex_size/100

grid_x_pixels = 0.8 * w
grid_y_pixels = 0.8 * h

sep_x = 3 * hex_size
sep_y = .86 * hex_size

grid_x = int(grid_x_pixels / sep_x) + 1
grid_y = int(grid_y_pixels / sep_y) + 1

pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", int(hex_size/2.2))
myfont2 = pygame.font.SysFont("Comic Sans MS", 30)

ar = [[0 for i in range(grid_x)] for j in range (grid_y)]

#naming the corners
leftmost_x = current_x = w/2.0 - grid_x_pixels/2.0
topmost_y = current_y = h/2.0 - grid_y_pixels/2.0

#initialize the matrix
for i in range(grid_y):
    if (i % 2 == 0):
        current_x += 1.5 * hex_size
    for j in range(grid_x):
        ar[i][j] = (current_x, current_y)
        current_x += sep_x
    current_x = w/2.0 - grid_x_pixels/2.0
    current_y += sep_y

rightmost_x = ar[0][-1][0] 
bottommost_y = ar[-1][-1][1]

def printAtCoord(x,y):
    xCoord = myfont.render(str(int(x)), False, (0, 0, 0))
    display.blit(xCoord, (x-hex_size/2,y-hex_size/2))
    yCoord = myfont.render(str(int(y)), False, (0, 0, 0))
    display.blit(yCoord, (x-hex_size/2,y-hex_size/5))
    
def move(add, key):
    x = add[0]
    y = add[1]
    if key == pygame.K_q and x != leftmost_x and y - topmost_y >= sep_y:
        x -= 1.5 * hex_size
        y -= sep_y
    elif key == pygame.K_w and y - topmost_y > sep_y:
        y -= 2 * sep_y
    elif key == pygame.K_e and  x!= rightmost_x and y - topmost_y >= sep_y:
        x += 1.5 * hex_size
        y -= sep_y
    elif key == pygame.K_a and x != leftmost_x and bottommost_y -y + epsilon >= sep_y:
        x -= 1.5 * hex_size
        y += sep_y
    elif key == pygame.K_s and bottommost_y -y > sep_y:
        y += 2 * sep_y
    elif key == pygame.K_d and x!= rightmost_x and bottommost_y -y + epsilon >= sep_y:
        x += 1.5 * hex_size
        y += sep_y
    return (x, y)

def draw_hexagon(x, y):
    side = hex_size
    v2 = (x + side * sin(PI/2), y + side * cos(PI/2))
    v3 = (x + side * sin(PI/6), y + side * cos(PI/6))
    v4 = (x + side * sin(11 * PI/6), y + side * cos(11 * PI/6))
    v5 = (x + side * sin(3 * PI/2), y + side * cos(3 * PI/2))
    v6 = (x + side * sin(7 * PI/6), y + side * cos(7 * PI/6))
    v1 = (x + side * sin(5 * PI/6), y + side * cos(5 * PI/6))
    vertices = [v1, v2, v3, v4, v5, v6, v1]
    for i in range(6):
        pygame.draw.line(display, (0, 0, 255), vertices[i], vertices[i+1])
    #putting the coordinates inside hexagonsd
    
    #printing the hex coordinates
    #printAtCoord(x,y)
   

def draw_objects(circ_add, target_add):
    pygame.draw.circle(display, (0, 0, 255), circ_add, hex_size/2)
    pygame.draw.circle(display, (255, 0, 0), target_add, hex_size/2)

# Create the Canvas
display = pygame.display.set_mode((w, h))
#pg.background(255)
display.fill((255, 255, 255))
    
# Higher resolution
"""
pg.pixelDensity(2)

Shape Details
pg.strokeWeight(2)
pg.stroke(0)
pg.noFill()
"""

#Circle object random coordinates
circ_x = random.randint(0, len(ar[0])-1)
circ_y = random.randint(0, len(ar)-1)

target_x = random.randint(0, len(ar[0])-1)
target_y = random.randint(0, len(ar)-1)

circ_add = (ar[circ_y][circ_x])
target_add = (ar[target_y][target_x])

arr = [circ_add]  #stores the path

def background():
    #display.fill((123,108,116)) #zoom background color
    display.fill((255, 255, 255)) #white
    #display.fill((0, 0, 0)) #black
    for ln in ar:
        for el in ln:
            draw_hexagon(el[0], el[1])
    #displaying the past path
    for i in range(len(arr)-1):
        pygame.draw.line(display, (0, 0, 0), arr[i], arr[i+1])
    #displaying the circles
    draw_objects(circ_add, target_add)

running = True
while running: 
    background() #draws the hexagonal space, circles and the path
    countText = myfont2.render(str(count), False, (0, 0, 0))
    display.blit(countText, (w*0.8,0))
    pygame.display.flip()
    
    #winning case
    if  abs(circ_add[0] - target_add[0]) < epsilon and abs(circ_add[1] - target_add[1]) < epsilon:
        pygame.draw.circle(display, (255, 0, 255), target_add, hex_size/2)
        winningText = myfont2.render("You won!", False, (0, 0, 0))
        display.blit(winningText, (0,0))
        pygame.display.flip()
        running = False
    
    elif count == 0:
        losingText = myfont2.render("You lost!", False, (0, 0, 0))
        display.blit(losingText, (0,0))
        pygame.display.flip()
        running = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             
            # checking if keydown event happened or not
            if event.type == pygame.KEYDOWN:
                old_add = circ_add
                circ_add = move(old_add, event.key)
                if circ_add != old_add: #to ensure that the circle has moved
                    count -= 1
                    arr.append(circ_add)
                    
        
        



