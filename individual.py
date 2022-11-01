from food import Food


class Individual:
    def __init__(self, lifetime, sight):

        self.lifetime = lifetime
        self.sight = sight

    # Represents an individual's action in one time step, given the circumstances
    def step(self, pos, env):
        x, y = pos
        fov = self.field_of_vision(pos)  # Find field of vision
        food = find_food(fov, env)  #
        print(food)
        if food:
            dist_x = food[0] - x
            dist_y = food[1] - y
            new_x = x
            new_y = y
            if abs(dist_x) >= abs(dist_y):
                print(dist_x / abs(dist_x))
                new_x = int(x + (dist_x / abs(dist_x)))
            else:
                print(dist_y / abs(dist_y))
                new_y = int(y + (dist_y / abs(dist_y)))

            # Check out of bounds
            if new_x < 0 or new_x >= env.grid_size or new_y < 0 or new_y >= env.grid_size:
                return

            # Check individual collision
            if isinstance(env.grid[new_x][new_y], Individual):
                return

            # If new space is food, add to lifetime!
            if isinstance(env.grid[new_x][new_y], Food):
                self.lifetime += 50  # TODO: Hardcoded value

            env.grid[x][y] = 0
            env.grid[new_x][new_y] = self

        else:
            new_x, new_y = random_pos(pos, env.rand)
            # Check out of bounds
            if new_x < 0 or new_x >= env.grid_size or new_y < 0 or new_y >= env.grid_size:
                return

            # Check individual collision
            if isinstance(env.grid[new_x][new_y], Individual):
                return

            env.grid[x][y] = 0
            env.grid[new_x][new_y] = self
        self.lifetime -= 1

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
def find_food(fov, env):
    for x, y in fov:
        # Check out of bounds
        if x < 0 or x >= env.grid_size or y < 0 or y >= env.grid_size:
            return

        if isinstance(env.grid[x][y], Food):
            return x, y
    return None

def random_pos(pos, rand):
    x, y = pos
    rand = rand.integers(0, 4)
    if rand == 0:
        return [x - 1, y]
    if rand == 1:
        return [x, y - 1]
    if rand == 2:
        return [x + 1, y]
    if rand == 3:
        return [x, y + 1]

    print(f"unhandled movement: {rand}")
    return [x, y]
