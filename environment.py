import pygame
import pygame.freetype
import numpy as np
from time import sleep

# Local
from food import Food
from individual import Individual
import params


class Environment:
    def __init__(self, seed=42):
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
        self.individuals = init_individuals(self)
        self.foods = init_foods(self)
        self.tick = 0

    def reset(self):
        self.init_variables()

    def step(self):
        for individual in self.individuals:
            individual.step(self)

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
            rect = pygame.Rect(x * block_size, y * block_size, block_size + 1, block_size + 1)
            pygame.draw.rect(screen, (0, env.background[x][y], 0), rect)             
            
            # Render text
            env.font.render_to(screen, (10, env.screen_size - 24), str(env.tick), (0, 0, 0))
    
    # Draw food
    for food in env.foods:
        food_x, food_y = food.position
        rect = pygame.Rect(food_x * block_size, food_y * block_size, block_size + 1, block_size + 1)
        pygame.draw.rect(screen, (227, 206, 18), rect)

    # Draw individuals
    for individual in env.individuals:
        pos = individual.position
        pygame.draw.circle(screen, (220, 0, 0), (pos[0] * block_size, pos[1] * block_size), block_size / 2)   

def init_background(env) -> list:
    background = []

    for x in range(env.grid_size):
        column = []
        for y in range(env.grid_size):
            column.append(env.rand.integers(150, 220))
        background.append(column)
    
    return background

def init_individuals(env) -> list:
    individuals = []

    for i in range(env.num_of_ind):
        x = env.rand.random() * (env.grid_size - 1) + 0.5
        y = env.rand.random() * (env.grid_size - 1) + 0.5
        individuals.append(Individual((x, y), params.LIFETIME, params.SIGHT_RANGE))

    return individuals

def init_foods(env) -> list:
    foods = []

    x_values = env.rand.choice(range(env.grid_size), size=env.num_of_food)
    y_values = env.rand.choice(range(env.grid_size), size=env.num_of_food)

    for i in range(env.num_of_food):
        foods.append(Food((x_values[i], y_values[i]), params.FOOD_NUTRITION))
    
    return foods