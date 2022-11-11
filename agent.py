# Class representing an agent in the simulation
import numpy as np
PI2 = 2 * np.pi


class Agent:
    energy              = 300   # Initial energy
    velocity            = 0.1   # Movement speed
    angular_velocity    = 0.2   # Rotation speed
    sight_range         = 50    # View distance in world

    def __init__(self, x, y, a, net):
        self.x = x
        self.y = y
        self.angle = a
        self.net = net

        self.age = 0

    # Move one step in time
    def step(self, env):
        # If the individual is out of energy, don't do anything
        if self.energy <= 0:
            return

        speed = 0
        angle = self.angle

        # Activate brain
        inputs = self.normalized_inputs(env)
        actions = self.net.activate(inputs)

        # Forward
        if actions[0] > env.rand.random():
            speed += self.velocity

        # Rotate left
        if actions[1] > env.rand.random():
            angle -= self.angular_velocity

        # Rotate right
        if actions[2] > env.rand.random():
            angle += self.angular_velocity

        # Calculate new position
        new_x = min(max(0, self.x + speed * np.cos(angle)), env.grid_size - 1)
        new_y = min(max(0, self.y + speed * np.sin(angle)), env.grid_size - 1)

        # Assign new values
        self.x = new_x
        self.y = new_y
        self.angle = angle % PI2
        self.age += 1
        self.energy -= 1 + speed ** 2

    def normalized_inputs(self, env):
        const = 1
        random = np.random.random()
        x = self.normalize(self.x, 0, env.grid_size - 1)
        y = self.normalize(self.y, 0, env.grid_size - 1)
        angle = self.normalize(self.angle, 0, PI2)
        age = self.normalize(self.angle, 0, env.steps)

        # Food
        food_dist, food_angle = self._find_nearest(env.foods)
        food_dist = self.normalize(food_dist, 0, self.sight_range)
        food_angle = self.normalize(food_angle, 0, PI2)

        return const, random, x, y, angle, age, food_dist, food_angle

    # Finds the nearest entity from a list of entities
    #   values: list of entities
    #   max_dist: maximum allowed distance
    # returns entity, distance and angle if there is a valid result, (None, max_dist, 0) if not.
    def _find_nearest(self, values):
        nodes = np.asarray(values)
        dist_2 = np.sum((nodes - (self.x, self.y)) ** 2, axis=1)
        nearest = np.argmin(dist_2)
        x, y = nodes[nearest]
        min_dist = np.sqrt(dist_2[nearest])

        # Return if the nearest entity is outside of view distance
        if min_dist > self.sight_range:
            return self.sight_range, 0

        # Calculate angle
        x -= self.x
        y += self.y
        angle = np.arctan2(y, x)

        return min_dist, angle

    def squared_dist_between(self, o) -> float:
        return (self.x - o[0]) ** 2 + (self.y - o[1]) ** 2

    # Normalizes a value
    @staticmethod
    def normalize(value, min, max):
        return np.divide(value - min, max - min)
