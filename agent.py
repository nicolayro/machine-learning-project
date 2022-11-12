# Class representing an agent in the simulation
import numpy as np
PI2 = 2 * np.pi


class Agent:
    initial_energy      = 400   # Initial energy
    sight_range         = 15    # View distance in world

    # x: x-coordinate
    # y: y-coordinate
    # a: angle (rad)
    # net: feed-forward neural network
    def __init__(self, x, y, a, net, species):
        self.x = x
        self.y = y
        self.angle = a
        self.net = net
        self.species = species

        self.age = 0
        self.energy = self.initial_energy

    # Move one step in time
    def step(self, env):
        self.age += 1
        self.energy -= 1

        # If the individual is out of energy, don't do anything
        if self.energy <= 0:
            return

        # Activate brain
        inputs = self.normalized_inputs(env)
        actions = self.net.activate(inputs)
        if len(actions) != 2:
            print(len(actions))

        speed = actions[0]
        angle = self.angle + actions[1]

        # Calculate new position
        self.x = min(max(0, self.x + speed * np.cos(angle)), env.grid_size - 1)
        self.y = min(max(0, self.y + speed * np.sin(angle)), env.grid_size - 1)

        # Assign new values
        self.angle = angle % PI2
        self.energy -= speed ** 2

    def normalized_inputs(self, env):
        const = 1
        # random = np.random.random()
        # x = self.normalize(self.x, 0, env.grid_size - 1)
        # y = self.normalize(self.y, 0, env.grid_size - 1)
        angle = self.normalize(self.angle, 0, PI2)
        age = self.normalize(self.angle, 0, env.steps)
        energy = self.normalize(self.energy, 0, self.initial_energy)

        # Food
        food_dist, food_angle = self._find_nearest(env.foods)
        food_dist = self.normalize(food_dist, 0, self.sight_range)
        food_angle = self.normalize(food_angle, 0, PI2)

        # Other agents
        other_dist, other_angle, same = self._find_nearest_other(env.agents)
        other_dist = self.normalize(other_dist, 0, self.sight_range)
        other_angle = self.normalize(other_angle, 0, PI2)

        return const, angle, food_angle, food_dist, other_dist, other_angle, same

    def _find_nearest_other(self, others):
        min_dist = self.sight_range
        nearest = None
        for o in others:
            dist = self.squared_dist_between((o.x, o.y))
            if dist < min_dist:
                min_dist = dist
                nearest = o

        if nearest is None:
            return self.sight_range, 0, 0

        x = nearest.x - self.x
        y = nearest.y - self.y
        angle = np.arctan2(y, x)
        angle = self.angle - angle
        same = int(self.species == nearest.species)

        return min_dist, angle, same


    # Finds the nearest entity from a list of entities
    #   values: list of entities
    #   max_dist: maximum allowed distance
    # returns entity, distance and angle if there is a valid result, (None, max_dist, 0) if not.
    def _find_nearest(self, values):
        # Return if given empty list
        if values.size == 0:
            return self.sight_range, 0

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
        y -= self.y
        angle = np.arctan2(y, x)
        angle = self.angle - angle

        return min_dist, angle

    def squared_dist_between(self, o) -> float:
        return (self.x - o[0]) ** 2 + (self.y - o[1]) ** 2

    # Normalizes a value
    @staticmethod
    def normalize(value, min, max):
        return np.divide(value - min, max - min)
