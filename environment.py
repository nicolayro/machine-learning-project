import pygame
import pygame.freetype
import numpy as np
from time import sleep
from food import Food
from entity.individual import Individual

class Environment:
    def __init__(self, grid_size=10, num_of_ind=5, num_of_food=10, ticks=1000, fps=10, seed=42):
        self.grid_size = grid_size
        self.num_of_ind = num_of_ind
        self.num_of_food = num_of_food
        self.ticks = ticks
        self.fps = fps
        self.seed = seed

        self.init_variables()
    
    def init_variables(self):
        self.background = init_background(self)
        self.grid = init_grid(self)
        self.tick = 0

    def reset(self):
        self.init_variables()

    def step(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] != 0:
                    self.grid[x][y].step((x, y), self)

    def render(self):
        pygame.init()
        self.screen_size = 800
        screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Gridworld")
        self.font = pygame.freetype.Font("./assets/VCR_OSD_MONO.ttf", 24)

        running = True

        while running and self.tick < self.ticks:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if self.fps != 0:
                sleep(1/self.fps)
            
            screen.fill((0, 0, 0))
            drawGrid(screen, self)
            pygame.display.flip()

            self.step()
            self.tick += 1
        
        pygame.quit()

def drawGrid(screen, env):
    block_size = env.screen_size / env.grid_size

    for x in range(env.grid_size):
        for y in range(env.grid_size):
            # Draw background
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            pygame.draw.rect(screen, (0, env.background[x][y], 0), rect)

            # Draw individuals
            if isinstance(env.grid[x][y], Individual):
                pygame.draw.circle(screen, (220, 0, 0), ((x + 0.5) * block_size, ((y + 0.5) * block_size)), block_size / 4)
            
            # Draw food
            if isinstance(env.grid[x][y], Food):
                rect = pygame.Rect((x + 0.25) * block_size, (y + 0.25) * block_size, block_size / 2, block_size / 2)
                pygame.draw.rect(screen, (227, 206, 18), rect)
            
            # Render text
            env.font.render_to(screen, (10, env.screen_size - 24), str(env.tick), (0, 0, 0))

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
        grid[x_values[i]][y_values[i]] = Individual(200, 5)
    
    # Generate food
    x_values = np.random.choice([x for x in range(env.grid_size) if x not in x_values], size=env.num_of_food)
    y_values = np.random.choice([y for y in range(env.grid_size) if y not in y_values], size=env.num_of_food)

    for i in range(env.num_of_food):
        grid[x_values[i]][y_values[i]] = Food()

    return grid
