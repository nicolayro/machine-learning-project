import pygame
import numpy as np
from time import sleep


class Renderer:
    screen_size = 800  # Height/Width of window in pixels
    fps         = 0    # Target frames per second

    def __init__(self, grid_size):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Gridworld")
        self.font = pygame.freetype.Font("./assets/VCR_OSD_MONO.ttf", 24)

        self.grid_size = grid_size
        self.background = self._init_background()
        self.tick = 0

    def render(self, env):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if self.fps != 0:
            sleep(1/self.fps)

        self.screen.fill((0, 0, 0))
        self._draw_grid(env)
        pygame.display.flip()

        # self.step()
        self.tick += 1

    def _draw_grid(self, env):
        block_size = self.screen_size / env.grid_size

        for x in range(env.grid_size):
            for y in range(env.grid_size):

                # Draw background
                rect = pygame.Rect(x * block_size, y * block_size, block_size + 1, block_size + 1)
                pygame.draw.rect(self.screen, (0, self.background[x][y], 0), rect)

                # Render text
                self.font.render_to(self.screen, (10, self.screen_size - 24), str(self.tick), (0, 0, 0))

        # Draw food
        for food in env.foods:
            food_x, food_y = food
            rect = pygame.Rect(food_x * block_size, food_y * block_size, block_size + 1, block_size + 1)
            pygame.draw.rect(self.screen, (227, 206, 18), rect)

        # Draw individuals
        for agent in env.agents:

            # TODO: Optimize :)
            value = min(255, max(0, agent.energy))
            red = (value, 0, 0)
            white = (255, 255, 255)
            black = (0, 0, 0)
            surface = pygame.Surface((block_size, block_size))

            # Transparent square
            surface.set_colorkey((255, 0, 255))
            surface.fill((255, 0, 255))

            # Create individual
            pygame.draw.circle(surface, red, (block_size / 2, block_size / 2), block_size / 2)
            pygame.draw.circle(surface, white, (3 * block_size / 4, block_size / 2), block_size / 5)
            pygame.draw.circle(surface, black, (3 * block_size / 4, block_size / 2), block_size / 10)

            # Rotate direction
            surface = pygame.transform.rotate(surface, agent.angle * - 57.296)  # convert to degrees
            self.screen.blit(surface, (agent.x * block_size, agent.y * block_size))

    def _init_background(self):
        background = []
        for x in range(self.grid_size):
            column = []
            for y in range(self.grid_size):
                column.append(np.random.randint(150, 220))
            background.append(column)

        return background

