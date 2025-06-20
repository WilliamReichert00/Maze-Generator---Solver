import pygame, math, time
from random import choice, shuffle

from pygame import K_SPACE
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_r,
    K_p,
    K_o,
    K_i
)

SCREENWIDTH = 2450
SCREENHEIGHT = 1250

GRIDSCALE = 50
mazeX = SCREENWIDTH // GRIDSCALE
mazeY = SCREENHEIGHT // GRIDSCALE

# produces a two-dimensional array of (int) x by y. array value [a][b] a value of 0 if the space is empty, a value of 1 if occupied wall
def makeMaze(x, y, starts=None):

    # make array
    if starts is None:
        starts = [-1, -1]
    maze = []
    visited = []
    for i in range(0,x):
        maze.append([])
        for j in range(0,y):
            maze[i].append((i*j)%2)
            if (i*j)%2 > 0:
                visited.append([i,j])

    # find start
    possible_point = []
    for i in range(0, len(maze)):
        if i%2 != 1:
            for j in range(0,len(maze[i])):
                if j%2 != 1:
                    possible_point.append([i, j])
    if starts in possible_point:
        start = starts
    else:
        start = choice(possible_point)

    visited.append(start)
    still_check = [[start, [0, 1, 2, 3]]]
    while len(still_check) > 0:
        # randomly checks [up down left right], checking walls and boundaries, if new space already visited: become wall, if no availible moves, check new position
        at = choice(still_check)
        while len(still_check) >= 1 and len(at[1]) > 0:
            looking = choice(at[1])
            at[1].remove(looking)
            if looking == 0:
                if at[0][0] > 0:
                    if [at[0][0]-1,at[0][1]] not in visited:
                        at = [[at[0][0]-1,at[0][1]],[0, 2, 3]]
                        visited.append(at[0])
                        still_check.append(at)
                    elif maze[at[0][0]-1][at[0][1]] != 1:
                        maze[at[0][0]][at[0][1]] = 1
                        still_check.remove(at)
                        at = choice(still_check)
            elif looking == 1:
                if at[0][0] < x-1:
                    if [at[0][0]+1,at[0][1]] not in visited:
                        at = [[at[0][0]+1,at[0][1]],[1, 2, 3]]
                        visited.append(at[0])
                        still_check.append(at)
                    elif maze[at[0][0]+1][at[0][1]] != 1:
                        maze[at[0][0]][at[0][1]] = 1
                        still_check.remove(at)
                        at = choice(still_check)
            elif looking == 2:
                if at[0][1] > 0:
                    if [at[0][0],at[0][1]-1] not in visited:
                        at = [[at[0][0],at[0][1]-1],[0, 1, 2]]
                        visited.append(at[0])
                        still_check.append(at)
                    elif maze[at[0][0]][at[0][1]-1] != 1:
                        maze[at[0][0]][at[0][1]] = 1
                        still_check.remove(at)
                        at = choice(still_check)
            elif looking == 3:
                if at[0][1] < y-1:
                    if [at[0][0],at[0][1]+1] not in visited:
                        at = [[at[0][0],at[0][1]+1],[0, 1, 3]]
                        visited.append(at[0])
                        still_check.append(at)
                    elif maze[at[0][0]][at[0][1]+1] != 1:
                        maze[at[0][0]][at[0][1]] = 1
                        still_check.remove(at)
                        at = choice(still_check)
        still_check.remove(at)

    # find end point
    possible_point = []
    for i in range(0, len(maze)):
        # skip checking initial walls row + columns
        if i % 2 != 1:
            for j in range(0, len(maze[i])):
                if j % 2 != 1:
                    # make sure point is not already a wall
                    if maze[i][j] != 1:
                        # only pick points in a corner, must have 3 adjacent walls/borders
                        edges = 0
                        if i == 0 or i+1 == x:
                            edges += 1
                        if i-1 >= 0:
                            if maze[i-1][j] == 1:
                                edges += 1
                        if i+1 < x:
                            if maze[i+1][j] == 1:
                                edges += 1
                        if j == 0 or j+1 == y:
                            edges += 1
                        if j-1 >= 0:
                            if maze[i][j-1] == 1:
                                edges += 1
                        if j+1 < y:
                            if maze[i][j+1] == 1:
                                edges += 1
                        if edges == 3:
                            possible_point.append([i, j])
    if starts in possible_point:
        possible_point.remove(starts)
    end = choice(possible_point)

    return [maze,start,end]

# returns a list of numbers 0-3 where the last element is the most desired direction to reduce distance between player and goal. can be intelligent or random
def direction_priority(player,goal,intelligent= True):
    if intelligent:
        dx = player[0] - goal[0]
        dy = player[1] - goal[1]
        left = False
        down = False
        pr_x = False
        temp = []
        if math.fabs(dx) > math.fabs(dy):  # prioritize x means put left/right value first. attempts to minimize lower value
            pr_x = True
        elif math.fabs(dx) - math.fabs(dy) == 0:
            pr_x = math.fabs(dx - mazeX//2) - math.fabs(dy - mazeY//2) < 0
        if dx > 0:  # if value greater than 0, prioritize left 0 over right 1, if dx = 0, prioritize closer x boundary
            left = True
        elif dx == 0:
            left = mazeX - player[0] < mazeX//2
        if dy > 0:  # if value greater than 0, prioritize down 2 over up 3 if dy = 0, prioritize closer y boundary
            down = True
        elif dy == 0:
            down = mazeY - player[1] > mazeY//2

        if pr_x:
            if left:
                temp += [1]
                if down:
                    temp += [3, 2]
                else:
                    temp += [2, 3]
                temp += [0]
            else:
                temp += [0]
                if down:
                    temp += [3, 2]
                else:
                    temp += [2, 3]
                temp += [1]
        else:
            if down:
                temp += [3]
                if left:
                    temp += [1,0]
                else:
                    temp += [0, 1]
                temp += [2]
            else:
                temp += [2]
                if left:
                    temp += [1, 0]
                else:
                    temp += [0, 1]
                temp += [3]

    else:
        temp = [0,1,2,3]
        shuffle(temp)

    return temp

# pygame screen definition
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
screen.fill((0, 0, 0))

maze,start,end = makeMaze(mazeX, mazeY)

player = start.copy(), [255,0,255]

loop = True # loop control variable
pause = False
draw = True
smart = True
x_mov = 0
y_mov = 0

auto_solve = False
next = direction_priority(player[0], end)
moves = 0
solves = 0
efficiency_storage = 0
while loop:
    screen.fill((25, 25, 0))

    # check inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                loop = False
            if event.key == K_r:
                maze,start,end = makeMaze(mazeX, mazeY)
                player[0][0],player[0][1] = start
                next = direction_priority(player[0], end, smart)
                efficiency_storage = 0
                solves = 0
                moves = 0

            if event.key == K_p:
                # check inputs
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            loop = False
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                loop = False
                                pause = False
                            if event.key == K_p:
                                pause = False
                break
            if event.key == K_o:
                draw = not draw
            if event.key == K_SPACE:
                auto_solve = not auto_solve
                next = [0,1,2,3]
            if event.key == K_i:
                smart = not smart
            if event.key == K_LEFT:
                x_mov -= 1
            if event.key == K_RIGHT:
                x_mov += 1
            if event.key == K_UP:
                y_mov -= 1
            if event.key == K_DOWN:
                y_mov += 1
        if event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                x_mov = 0
            if event.key == K_RIGHT:
                x_mov = 0
            if event.key == K_UP:
                y_mov = 0
            if event.key == K_DOWN:
                y_mov = 0

    # draw maze walls
    if draw:
        for i in range(0,len(maze)):
            for j in range(0,len(maze[i])):
                if maze[i][j] == 1:
                    pygame.draw.rect(screen, (25,100,15),rect=pygame.Rect(i*GRIDSCALE, j*GRIDSCALE, GRIDSCALE, GRIDSCALE))

        # mark start and end
        pygame.draw.rect(screen, (75, 25, 75), rect=pygame.Rect(start[0] * GRIDSCALE, start[1] * GRIDSCALE, GRIDSCALE, GRIDSCALE))
        pygame.draw.rect(screen, (175, 100, 120), rect=pygame.Rect(end[0] * GRIDSCALE, end[1] * GRIDSCALE, GRIDSCALE, GRIDSCALE))

        pygame.draw.rect(screen, player[1], rect=pygame.Rect(player[0][0]*GRIDSCALE, player[0][1]*GRIDSCALE, GRIDSCALE, GRIDSCALE))

    if auto_solve:
        again = True
        while again:
            if len(next) > 0:
                pick = next.pop(-1)
                x_mov = 0
                y_mov = 0
                if pick == 0 and 0 <= player[0][0] - 1:
                    if maze[player[0][0] - 1][player[0][1]] != 1:
                        next.append(4)

                        temp = direction_priority(player[0], end, smart)

                        temp.remove(1)
                        next += temp
                        x_mov = -1
                        y_mov = 0
                        again = False
                elif pick == 1 and player[0][0] + 1 < mazeX:
                    if maze[player[0][0] + 1][player[0][1]] != 1:
                        next.append(5)

                        temp = direction_priority(player[0],end, smart)

                        temp.remove(0)
                        next += temp
                        x_mov = 1
                        y_mov = 0
                        again = False
                elif pick == 2 and 0 <= player[0][1] - 1:
                    if maze[player[0][0]][player[0][1] - 1] != 1:
                        next.append(6)

                        temp = direction_priority(player[0], end, smart)

                        temp.remove(3)
                        next += temp
                        x_mov = 0
                        y_mov = -1
                        again = False
                elif pick == 3 and player[0][1] + 1 < mazeY:
                    if maze[player[0][0]][player[0][1] + 1] != 1:
                        next.append(7)

                        temp = direction_priority(player[0], end, smart)

                        temp.remove(2)
                        next += temp
                        x_mov = 0
                        y_mov = 1
                        again = False

                elif pick == 4 and 0 < player[0][0] + 1 < mazeX:
                    if maze[player[0][0] + 1][player[0][1]] != 1:
                        x_mov = 1
                        y_mov = 0
                        again = False
                    else:
                        print("huh?")
                elif pick == 5 and 0 <= player[0][0] - 1:
                    if maze[player[0][0] - 1][player[0][1]] != 1:
                        x_mov = -1
                        y_mov = 0
                        again = False
                    else:
                        print("huh?")
                elif pick == 6 and player[0][1] + 1 < mazeY:
                    if maze[player[0][0]][player[0][1] + 1] != 1:
                        x_mov = 0
                        y_mov = 1
                        again = False
                    else:
                        print("huh?")
                elif pick == 7 and 0 <= player[0][1] - 1:
                    if maze[player[0][0]][player[0][1] - 1] != 1:
                        x_mov = 0
                        y_mov = -1
                        again = False
                    else:
                        print("huh?")

    # handle player movement
    if x_mov != 0 and 0 <= player[0][0] + x_mov < mazeX:
        if maze[player[0][0] + x_mov][player[0][1]] != 1:
            player[0][0] += x_mov
            moves += 1
    if y_mov != 0 and 0 <= player[0][1] + y_mov < mazeY:
        if maze[player[0][0]][player[0][1]+y_mov] != 1:
            player[0][1] += y_mov
            moves += 1
    if player[0] == end:
        solves += 1
        print("solved in ", moves, "moves!")
        if auto_solve:
            potential = next.count(4) + next.count(5) + next.count(6) + next.count(7)
            efficiency = potential / moves * 100
            efficiency_storage += efficiency
            print("could have been solved in ", potential, " moves!")
            print("efficiency:", efficiency, "%")
            print("average efficiency: ", efficiency_storage / solves, "%")
        moves = 0
        maze,start,end = makeMaze(mazeX, mazeY,starts=end)
        next = direction_priority(player[0], end, smart)

    # apply screen changes
    pygame.display.flip()
    if draw:
        time.sleep(30/1000)