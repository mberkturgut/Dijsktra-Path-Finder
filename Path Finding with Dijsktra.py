from math import sin, cos, pi as PI
import pygame
import random
import sys
import heapq as heap
from collections import deque
import time

gridSize = 500
w = h = gridSize

hex_size = 20
epsilon = hex_size/100

grid_x_pixels = 0.8 * w
grid_y_pixels = 0.8 * h

sep_x = 3 * hex_size
sep_y = .86 * hex_size

grid_x = int(grid_x_pixels / sep_x) + 1
grid_y = int(grid_y_pixels / sep_y) + 1
totalSize = grid_x * grid_y
obs_ratio = 0.6
nofObs = int(obs_ratio * totalSize)


pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", int(hex_size/2.2))
myfont2 = pygame.font.SysFont("Comic Sans MS", 30)

ar = [[0 for i in range(grid_x)] for j in range (grid_y)]

#naming the corners
leftmost_x = current_x = w/2.0 - grid_x_pixels/2.0
topmost_y = current_y = h/2.0 - grid_y_pixels/2.0

#initialize the address matrix
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
    
def printTextAtCoord(txt, x,y):
    xCoord = myfont.render(txt, False, (0, 0, 0))
    display.blit(xCoord, (x-hex_size/2,y-hex_size/3))
    
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
    #printing the coordinates inside hexagons
    #printAtCoord(x,y)

def draw_objects(circ_add, target_add, obs_adds):
    pygame.draw.circle(display, (0, 0, 255), circ_add, hex_size/2)
    pygame.draw.circle(display, (255, 0, 0), target_add, hex_size/2)
    for el in obs_adds:
        pygame.draw.circle(display, (0, 0, 0), ar[el[1]][el[0]], hex_size/2)
# Create the Canvas
display = pygame.display.set_mode((w, h))
#pg.background(255)
display.fill((255, 255, 255))
    
    # Higher resolution
    # pg.pixelDensity(2)
    
    # Shape Details
    #pg.strokeWeight(2)
    #pg.stroke(0)
    #pg.noFill()
    
#Circle object random coordinates
circ_x = random.randint(0, len(ar[0])-1)
circ_y = random.randint(0, len(ar)-1)

target_x = random.randint(0, len(ar[0])-1)
target_y = random.randint(0, len(ar)-1)

target_x = 0
target_y = 5
while ((circ_x, circ_y) == (target_x,target_y)):
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
    draw_objects(circ_add, target_add, obs)

def ifPossible(x, y): #checks if the desired index is in the grid
    if x > grid_x -1 or x < 0 or y > grid_y-1 or y < 0:
        return False
    return True

#creating obstacles
obs = []
for i in range(nofObs):
    el = (random.randint(0, len(ar[0])-1), random.randint(0, len(ar)-1))
    if el != (circ_x, circ_y) and el != (target_x, target_y):
        obs.append(el)

def adj(x,y): 
    adjl = []
    if(y%2 == 0):       
        if (ifPossible(x, y-2)):
            adjl.append((x,y-2))
        if (ifPossible(x, y-1)):
            adjl.append((x, y-1))
        if (ifPossible(x, y+1)):
            adjl.append((x, y+1))
        if (ifPossible(x, y+2)):
            adjl.append((x, y+2))
        if (ifPossible(x + 1, y-1)):
            adjl.append((x + 1, y-1))
        if (ifPossible(x + 1, y +1)):
            adjl.append((x + 1, y+1))
    else:
        if (ifPossible(x, y-2)):
            adjl.append((x, y-2))
        if (ifPossible(x , y-1)):
            adjl.append((x, y-1))
        if (ifPossible(x, y+1)):
            adjl.append((x, y+1))
        if (ifPossible(x, y+2)):
            adjl.append((x, y+2))
        if (ifPossible(x - 1, y - 1)):
            adjl.append((x - 1, y - 1))
        if (ifPossible(x - 1, y + 1)):
            adjl.append((x - 1, y + 1))
    for el in obs:
        if el in adjl:
            adjl.remove(el)
    return adjl

adjList = [[adj(x, y) for x in range(grid_x)] for y in range (grid_y)] #Adjacency list initilization

def trace(dest, src, parents):
    stack = deque()
    destination_x = dest[0]
    destination_y = dest[1]
    x = src[0]
    y = src[1]

    while((x,y) != (destination_x,destination_y)):
        parent = parents[y][x]
        x = parent[0]
        y = parent[1]
        stack.append(parent)

    path = []
    while len(stack) > 0:
        path.append(stack.pop())

    path.append(src)
    return path

distance = [[float('inf') for i in range(grid_x)] for j in range(grid_y)]

parents_map = [[-1 for i in range(grid_x)] for j in range(grid_y)]

def dijkstra(adjList, circ_x, circ_y):
    global isReachable
    isReachable = True
    distance[circ_y][circ_x] = 0
    visited = set()
    global parents_map
    pq = []
    start = (circ_x, circ_y)
    heap.heappush(pq, (0, start))

    while pq:
        dist, node = heap.heappop(pq)
        #print("node", node)
        visited.add(node)
        x = node[0]
        y= node[1]
        adjl = adjList[y][x]
        time.sleep(0.12)
        #    background()
            
        #showing the adjacents on the grid
        #for el in adjl:
        #   coord = ar[el[1]][el[0]]
        #   printAtCoord(coord[0], coord[1])             
        for neighbor in adjl:         
            if neighbor not in visited:
                new_distance = distance[y][x] + 1#node to node distance
                #print("Neighbor", neighbor[0], neighbor[1])
                old_distance = distance[neighbor[1]][neighbor[0]]
                if new_distance < old_distance:
                    parents_map[neighbor[1]][neighbor[0]] = node
                    distance[neighbor[1]][neighbor[0]] = new_distance
                    heap.heappush(pq, (new_distance, neighbor))
        printTextAtCoord(str(distance[y][x]), ar[y][x][0], ar[y][x][1])    
        pygame.display.flip()
        if (target_x, target_y) in visited:
            break
    #print(len(visited))
    if (target_x, target_y) not in visited:
        isReachable = False
    return parents_map

def getDist(src, dest):
    dijkstra(adjList, src[0], src[1])
    return distance[dest[1]][dest[0]]


background()

#dijkstra
dijkstra(adjList, circ_x, circ_y)
if isReachable:
    shortest = trace((circ_x, circ_y), (target_x, target_y), dijkstra(adjList, circ_x, circ_y))
    for i in range(len(shortest)-1):
       pygame.draw.line(display, (0, 0, 0), ar[shortest[i][1]][shortest[i][0]], ar[shortest[i+1][1]][shortest[i+1][0]])
    pathLength = len(shortest) -1
    valText = myfont2.render(str(pathLength), False, (0, 0, 0))
    display.blit(valText, (w*0.8,0))
else: 
    unreachableText = myfont2.render("Unreachable!", False, (0, 0, 0))
    display.blit(unreachableText, (w*0.6,0))

#A*
#heuristicLen = 



#game
pygame.display.flip()
count = 100
running = False
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


