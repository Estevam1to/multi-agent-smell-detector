# Game of life written in Python by GitHub Copilot

import pygame
import random
import numpy as np

# initialize pygame
pygame.init()

# set the width and height of the screen
width, height = 1000, 1000

# create the screen
screen = pygame.display.set_mode((width, height))

# set the title and icon
pygame.display.set_caption('Game of Life')

# set the background color
background = (0, 0, 0)

# set the cell color
cell_color = (255, 255, 255)

# set the number of cells
n_cells = 100

# set the cell size
cell_size = width / n_cells

# set the grid
grid = np.zeros((n_cells, n_cells))

# set the initial state of the grid
def set_initial_state():

    # loop through each cell
    for x in range(n_cells):
        for y in range(n_cells):

            # set the state of the cell
            if random.randint(0, 1) == 0:
                grid[x, y] = 1

# set the initial state of the grid
set_initial_state()

# get the number of neighbors
def get_neighbors(x, y):
    
        # set the number of neighbors
        n_neighbors = 0
    
        # loop through each neighbor
        for i in range(-1, 2):
            for j in range(-1, 2):
    
                # get the neighbor
                neighbor = grid[(x + i) % n_cells, (y + j) % n_cells]
    
                # increment the number of neighbors
                n_neighbors += neighbor
    
        # decrement the number of neighbors
        n_neighbors -= grid[x, y]
    
        # return the number of neighbors
        return n_neighbors

# get the next state of the grid
def get_next_state():
        
        # set the next state of the grid
        next_state = np.copy(grid)
        
        # loop through each cell
        for x in range(n_cells):
            for y in range(n_cells):
        
                # get the number of neighbors
                n_neighbors = get_neighbors(x, y)
        
                # set the next state of the cell
                if grid[x, y] == 0 and n_neighbors == 3:
                    next_state[x, y] = 1
                elif grid[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    next_state[x, y] = 0
        
        # return the next state of the grid
        return next_state

# set the running state
running = True

# game loop
while running:

    # set the background color
    screen.fill(background)

    # loop through each event
    for event in pygame.event.get():

        # check if the event is quit
        if event.type == pygame.QUIT:

            # set the running state
            running = False

    # loop through each cell
    for x in range(n_cells):
        for y in range(n_cells):

            # set the state of the cell
            if grid[x, y] == 1:

                # draw the cell
                pygame.draw.rect(screen, cell_color, (x * cell_size, y * cell_size, cell_size, cell_size))

    # update the grid
    grid = get_next_state()

    # update the screen
    pygame.display.update()

# quit pygame
pygame.quit()