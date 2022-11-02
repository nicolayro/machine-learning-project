import pygame
import pygame.freetype
import copy
import numpy as np

# Local
from time import sleep
from food import Food
from individual import Individual
import params


class Environment:
    def __init__(self):
        self.grid_size = params.GRID_SIZE
        self.num_of_ind = params.NUM_IND
        self.num_of_food = params.NUM_FOOD
        self.ticks = params.TICKS
        self.fps = params.FPS
        self.seed = params.SEED

        self.init_variables()
    
    def init_variables(self):
        self.rand = np.random.default_rng(self.seed)
        self.background = init_background(self)
        self.grid = init_grid(self)
        self.tick = 0

    def reset(self):
        self.init_variables()

    def step(self):
        original_grid = copy.deepcopy(self.grid)

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if original_grid[x][y] != 0:
                    original_grid[x][y].step((x, y), self)

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
            rect = pygame.Rect(x * block_size, y * block_size, block_size + 1, block_size + 1)

            # Draw food or background
            if isinstance(env.grid[x][y], Food):
                pygame.draw.rect(screen, (227, 206, 18), rect)
            else:
                pygame.draw.rect(screen, (0, env.background[x][y], 0), rect)
            
            # Draw individuals
            if isinstance(env.grid[x][y], Individual):
                pygame.draw.circle(screen, (220, 0, 0), ((x + 0.5) * block_size, ((y + 0.5) * block_size)), block_size / 2)
            
            # Render text
            env.font.render_to(screen, (10, env.screen_size - 24), str(env.tick), (0, 0, 0))

def init_background(env) -> list:
    background = []

    for x in range(env.grid_size):
        column = []
        for y in range(env.grid_size):
            column.append(env.rand.integers(150, 220))
        background.append(column)
    
    return background

def init_grid(env) -> list:
    grid = []

    # Initialize empty grid
    for x in range(env.grid_size):
        column = []
        for y in range(env.grid_size):
            column.append(0)
        grid.append(column)

    # Generate individuals
    x_values = env.rand.choice(range(env.grid_size), size=env.num_of_ind)
    y_values = env.rand.choice(range(env.grid_size), size=env.num_of_ind)

    for i in range(env.num_of_ind):
        grid[x_values[i]][y_values[i]] = Individual(params.LIFETIME, params.SIGHT_RANGE)
    
    # Generate food
    x_values = env.rand.choice([x for x in range(env.grid_size) if x not in x_values], size=env.num_of_food)
    y_values = env.rand.choice([y for y in range(env.grid_size) if y not in y_values], size=env.num_of_food)

    for i in range(env.num_of_food):
        grid[x_values[i]][y_values[i]] = Food()

    return grid
