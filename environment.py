import pygame
import pygame.freetype
import numpy as np
from time import sleep

# Local
from food import Food
from indiv import Indiv
import params


class Environment:
    def __init__(self):
        self.state = 0
        self.grid_size = params.GRID_SIZE
        self.num_of_ind = params.NUM_IND
        self.num_of_food = params.NUM_FOOD
        self.ticks = params.TICKS
        self.fps = params.FPS
        self.seed = params.SEED

        self._init_variables()
        self._init_pygame()

    def _init_variables(self):
        self.rand = np.random.default_rng(self.seed)
        self.background = self._init_background()
        self.individuals = self._init_individuals()
        self.foods = self._init_foods()
        self.tick = 0

    def _init_pygame(self):
        pygame.init()
        self.screen_size = 700
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Gridworld")
        self.font = pygame.freetype.Font("./assets/VCR_OSD_MONO.ttf", 24)

    def reset(self):
        self._init_variables()

    def step(self, ):
        for individual in self.individuals:
            individual.step(self)

    def render(self):

        running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if self.fps != 0:
            sleep(1/self.fps)

        self.screen.fill((0, 0, 0))
        self._draw_grid()
        pygame.display.flip()

        # self.step()
        self.tick += 1

    def _draw_grid(self):
        block_size = self.screen_size / self.grid_size

        for x in range(self.grid_size):
            for y in range(self.grid_size):

                # Draw background
                rect = pygame.Rect(x * block_size, y * block_size, block_size + 1, block_size + 1)
                pygame.draw.rect(self.screen, (0, self.background[x][y], 0), rect)

                # Render text
                self.font.render_to(self.screen, (10, self.screen_size - 24), str(self.tick), (0, 0, 0))

        # Draw food
        for food in self.foods:
            food_x, food_y = food.position
            rect = pygame.Rect(food_x * block_size, food_y * block_size, block_size + 1, block_size + 1)
            pygame.draw.rect(self.screen, (227, 206, 18), rect)

        # Draw individuals
        for individual in self.individuals:
            pos = individual.pos

            # TODO: Optimize :)
            value = min(255, max(0, individual.energy))
            red = (value, 0, 0)
            white = (255, 255, 255)
            black = (0, 0, 0)
            surface = pygame.Surface((block_size, block_size))

            # Transparent square
            surface.set_colorkey((255, 0, 255))
            surface.fill((255, 0, 255))

            # Create individual
            pygame.draw.circle(surface, red, (block_size / 2, block_size / 2), block_size / 2)  # draw the circle in the correct color
            pygame.draw.circle(surface, white, (3 * block_size / 4, block_size / 2), block_size / 5)  # draw the circle in the correct color
            pygame.draw.circle(surface, black, (3 * block_size / 4, block_size / 2), block_size / 10)  # draw the circle in the correct color

            # Rotate direction
            surface = pygame.transform.rotate(surface, individual.angle * -57.296)  # convert to degrees
            self.screen.blit(surface, (pos[0] * block_size, pos[1] * block_size))


    def _init_background(self) -> list:
        background = []
        for x in range(self.grid_size):
            column = []
            for y in range(self.grid_size):
                column.append(self.rand.integers(150, 220))
            background.append(column)

        return background

    def _init_individuals(self) -> list:
        individuals = []
        for i in range(self.num_of_ind):
            x = self.rand.random() * (self.grid_size - 1) + 0.5
            y = self.rand.random() * (self.grid_size - 1) + 0.5
            angle = self.rand.random() * 2 * np.pi
            individuals.append(Indiv((x, y), angle))

        return individuals

    def _init_foods(self) -> list:
        foods = []
        x_values = self.rand.choice(range(1, self.grid_size - 1), size=self.num_of_food)
        y_values = self.rand.choice(range(1, self.grid_size - 1), size=self.num_of_food)

        for i in range(self.num_of_food):
            foods.append(Food((x_values[i], y_values[i]), params.FOOD_NUTRITION))

        return foods
