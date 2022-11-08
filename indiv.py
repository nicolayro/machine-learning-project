import params
import numpy as np

import params

# Individual in the environment
class Indiv:

    def __init__(self, pos, angle):
        # Inputs
        self.pos = pos
        self.speed = 0
        self.angle = angle
        self.move_speed = 0.3
        self.angular_speed = 0.2
        self.age = 0
        self.energy = 300

    def inputs(self, env):
        return 1, (self.speed / self.move_speed), (self.angle / np.pi), self._find_angle_to_food(env), (self.age / params.EPISODE_LENGTH)

    def execute_action(self, action):
        self.energy -= 1
        self.age += 1

        # If the individual is out of food, don't do anything
        if self.energy <= 0:
            return

        # Add the vectors to the position
        speed = ((action[0] + 1) / 2) * self.move_speed
        angle = self.angle + action[1] * self.angular_speed

        new_pos = (self.pos[0] + speed * np.cos(angle), self.pos[1] + speed * np.sin(angle))

        # Wrap around angle
        if angle > np.pi:
            angle -= np.pi * 2
        elif angle < -np.pi:
            angle += np.pi * 2

        # Check x
        if new_pos[0] < 0:
            new_pos = (0, new_pos[1])
        elif new_pos[0] >= params.GRID_SIZE:
            new_pos = (params.GRID_SIZE - 0.5, new_pos[1])

        # Check y
        if new_pos[1] < 0:
            new_pos = (new_pos[0], 0)
        elif new_pos[1] >= params.GRID_SIZE:
            new_pos = (new_pos[0], params.GRID_SIZE - 0.5)

        self.pos = new_pos
        self.speed = speed
        self.angle = angle
        self.energy -= speed ** 2

    def _find_angle_to_food(self, env):
        min_dist = 100
        nearest_food = None

        for food in env.foods:
            dist = self.dist_squared(self.pos, food.position)
            if dist < min_dist:
                min_dist = dist
                nearest_food = food
        
        if nearest_food is None:
            return 0
        else:
            return (self.angle - self.angle_between(self.pos, nearest_food.position)) / (2 * np.pi)
    
    @staticmethod
    def angle_between(a, b) -> float:
        c = [b[0] - a[0], b[1] - a[1]]

        return np.arctan2(c[1], c[0])  

    @staticmethod
    def dist_squared(a, b) -> float:
        return (a[0]-b[0])**2 + (a[1]-b[1])**2

    @staticmethod
    def _normalize(value, max_value):
        return value / max_value
