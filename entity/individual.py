import numpy as np


class Individual(Entity):
    def __init__(self, lifetime, sight):

        self.lifetime = lifetime
        self.sight = sight

    # Represents an individual's action in one time step, given the circumstances
    def step(self, pos, env):
        fov = self.field_of_vision(pos)
        if sees_food(fov):
            # Move towards food
            pass
        else:
            env[pos] = 0
            movement = random_movement(env.seed)
            env[pos + movement] = self

    # Calculates field of vision for an individual relative to a given position
    def field_of_vision(self, pos):
        # Returns coordinates for a circle
        circle = []
        X = int(self.sight + 1)
        r = int(self.sight + 1)
        for x in range(-X, X + 1):
            Y = int((r * r - x * x) ** 0.5)
            if Y == 0:
                continue
            if Y > self.sight:
                Y = self.sight
            for y in range(-Y, Y + 1):
                circle.append([pos[0] + x, pos[1] + y])
        return circle


# Looks for food in the given area, returns true if there is food
def sees_food(area):
        return False



def random_movement(seed):
    np.random.seed(seed)
    rand = np.random.randint(5)
    if rand == 0:
        return [-1, 0]
    if rand == 1:
        return [0, -1]
    if rand == 2:
        return [1, 0]
    if rand == 3:
        return [0, 1]

    print(f"unhandled movement: {rand}")
    return [0, 0]
