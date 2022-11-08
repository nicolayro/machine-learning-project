import params
import numpy as np

# Individual in the environment
class Indiv:

    def __init__(self, pos, angle, speed):
        # Inputs
        self.pos = pos
        self.angle = angle
        self.speed = speed
        self.age = 0
        self.energy = 299

    def inputs(self, env):
        x, y = self._find_food(env)
        x -= self.pos[0]
        y -= self.pos[1]
        return self.pos[0], self.pos[1], self.angle, self.age, np.random.random(), 1, x, y

    def execute_action(self, action):
        self.energy -= 1

        # If the individual is out of food, don't do anything
        if self.energy <= 0:
            return

        self.age += 1

        # Add the vectors to the position
        speed = action[0] + 1
        angle = self.angle + action[1] * np.pi
        new_pos = (self.pos[0] + speed * np.sin(angle), self.pos[1] + speed * np.cos(angle))

        # Check x
        if new_pos[0] < 0:
            new_pos = (0, new_pos[1])
        elif new_pos[0] >= params.GRID_SIZE:
            new_pos = (params.GRID_SIZE - 1, new_pos[1])

        # Check y
        if new_pos[1] < 0:
            new_pos = (new_pos[0], 0)
        elif new_pos[1] >= params.GRID_SIZE:
            new_pos = (new_pos[0], params.GRID_SIZE - 1)

        self.pos = new_pos
        self.angle = angle
        self.energy -= speed ** 2


    def move(self, movement):
        pass

    def _find_food(self, env):
        min_dist = 10
        nearest_food = None

        for food in env.foods:
            dist = self.dist_between(self.pos, food.position)
            if dist < min_dist:
                min_dist = dist
                nearest_food = food
        return nearest_food.position if nearest_food is not None else (0, 0)

    @staticmethod
    def dist_between(a, b) -> float:
        return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    @staticmethod
    def _normalize(value, max_value):
        return value / max_value
