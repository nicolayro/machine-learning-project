import params
import numpy as np


# Individual in the environment
class Indiv:
    MAX_ENERGY = params.EPISODE_LENGTH
    SIGHT_RANGE = params.SIGHT_RANGE
    SPEED = params.SPEED

    def __init__(self, pos, angle, speed):
        # Inputs
        self.pos = pos
        self.angle = angle
        self.speed = speed

        self.age = 0
        self.energy = self.MAX_ENERGY

    def inputs(self, env):
        # Normalize values
        pos_x = self._normalize(self.pos[0], params.GRID_SIZE)
        pos_y = self._normalize(self.pos[1], params.GRID_SIZE)
        angle = self._normalize(self.angle, 2 * np.pi)
        age = self._normalize(self.age, params.EPISODE_LENGTH)
        energy = self._normalize(self.energy, self.MAX_ENERGY)
        random = np.random.random()

        # Relative position of the nearest food
        food_dist, food_angle = self._find_nearest(env.foods, self.SIGHT_RANGE)
        indiv_dist, indiv_angle = self._find_nearest(env.individuals, self.SIGHT_RANGE)

        food_angle = self._normalize(food_angle, 2 * np.pi)
        food_dist = self._normalize(food_dist, self.SIGHT_RANGE)
        indiv_dist = self._normalize(indiv_dist, 2 * np.pi)
        indiv_angle = self._normalize(indiv_angle, self.SIGHT_RANGE)

        return pos_x, pos_y, angle, age, energy, random, 1, food_angle, food_dist, indiv_angle, indiv_dist

    def execute_action(self, action):
        self.energy -= 1
        self.age += 1

        # If the individual is out of food, don't do anything
        if self.energy <= 0:
            return

        # Add the vectors to the position
        speed = action[0] * self.SPEED
        angle = self.angle + (action[1] - action[2]) * np.pi / 2
        new_pos = (self.pos[0] + speed * np.cos(angle), self.pos[1] + speed * np.sin(angle))

        # Check x
        if new_pos[0] < 0:
            new_pos = (0, new_pos[1])
        elif new_pos[0] >= params.GRID_SIZE - 1:
            new_pos = (params.GRID_SIZE - 1, new_pos[1])

        # Check y
        if new_pos[1] < 0:
            new_pos = (new_pos[0], 0)
        elif new_pos[1] >= params.GRID_SIZE - 1:
            new_pos = (new_pos[0], params.GRID_SIZE - 1)

        # Fix angle
        if angle > 2 * np.pi:
            angle -= 2 * np.pi
        elif angle < 0:
            angle += 2 * np.pi

        self.angle = angle
        self.pos = new_pos
        self.energy -= speed ** 2

    # Finds the nearest entity from a list of entities
    #   values: list of entities
    #   max_dist: maximum allowed distance
    # returns distance and angle if there is a valid result, (max_dist, 0) if not.
    def _find_nearest(self, values, max_dist):
        min_dist = max_dist
        nearest = None

        # Find the nearest
        for v in values:
            dist = self.dist_between(self.pos, v.pos)
            if dist < min_dist:
                min_dist = dist
                nearest = v

        # Return if there is no valid result
        if nearest is None:
            return max_dist, 0

        # Calculate angle
        x, y = (nearest.pos[0] - self.pos[0], nearest.pos[1] - self.pos[1])
        angle = np.arctan2(y, x)

        return min_dist, angle

    @staticmethod
    def dist_between(a, b) -> float:
        return np.sqrt((a[0]-b[0]) ** 2 + (a[1]-b[1]) ** 2)

    @staticmethod
    def _normalize(value, max_value):
        return value / max_value
