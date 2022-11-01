import pygame
import numpy as np
from time import sleep

class Environment:
    def __init__(self, grid_size=10, num_of_ind=5, num_of_food=10, seed=42):
        self.grid_size = grid_size
        self.num_of_ind = num_of_ind
        self.num_of_food = num_of_food
        self.seed = seed

        self.init_variables()
    
    def init_variables(self):
        self.background = init_background(self)
        self.grid = init_grid(self)

    def reset(self):
        self.init_variables()

    def step(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] != 0:
                    pass    # Todo: Replace with call to step() in Individual/Food

    def render(self):
        pygame.init()
        screen_size = 800
        screen = pygame.display.set_mode((screen_size, screen_size))
        self.block_size = screen_size / self.grid_size
        pygame.display.set_caption("Gridworld")

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            sleep(0.1)
            screen.fill((0, 0, 0))
            drawGrid(screen, self)
            pygame.display.flip()
        
        pygame.quit()

def drawGrid(screen, env):
    for x in range(env.grid_size):
        for y in range(env.grid_size):
            # Draw background
            rect = pygame.Rect(x * env.block_size, y * env.block_size, env.block_size, env.block_size)
            pygame.draw.rect(screen, (0, env.background[x][y], 0), rect)

            # Draw individuals
            if env.grid[x][y] == 1:     # Todo: Replace with comparison to Individual class
                pygame.draw.circle(screen, (220, 0, 0), ((x + 0.5) * env.block_size, ((y + 0.5) * env.block_size)), env.block_size / 4)
            
            # Draw food
            if env.grid[x][y] == 2:     # Todo: Replace with comparison to Food class
                rect = pygame.Rect((x + 0.25) * env.block_size, (y + 0.25) * env.block_size, env.block_size / 2, env.block_size / 2)
                pygame.draw.rect(screen, (227, 206, 18), rect)

def init_background(env) -> list:
    background = []
    np.random.seed(env.seed)

    for x in range(env.grid_size):
        column = []
        for y in range(env.grid_size):
            column.append(np.random.randint(150, 220))
        background.append(column)
    
    return background

def init_grid(env) -> list:
    grid = []
    np.random.seed(env.seed)

    # Initialize empty grid
    for x in range(env.grid_size):
        column = []
        for y in range(env.grid_size):
            column.append(0)
        grid.append(column)

    # Generate individuals
    x_values = np.random.choice(range(env.grid_size), size=env.num_of_ind)
    y_values = np.random.choice(range(env.grid_size), size=env.num_of_ind)

    for i in range(env.num_of_ind):
        grid[x_values[i]][y_values[i]] = 1  # Todo: Create Individual
    
    # Generate food
    x_values = np.random.choice([x for x in range(env.grid_size) if x not in x_values], size=env.num_of_food)
    y_values = np.random.choice([y for y in range(env.grid_size) if y not in y_values], size=env.num_of_food)

    for i in range(env.num_of_food):
        grid[x_values[i]][y_values[i]] = 2  # Todo: Create Food

    return grid