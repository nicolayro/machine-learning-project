import numpy as np


# Individual in the environment
class Indiv:
    energy              = 300   # Initial energy
    move_speed          = 0.3   # Movement speed
    angular_speed       = 0.2   # Rotation speed
    sight_range         = 15    # View distance in world

    def __init__(self, x, y, angle, net):
        self.x = x
        self.y = y
        self.angle = angle
        self.net = net

        self.speed = 0
        self.age = 0

    def normalized_inputs(self, env):
        const = 1
        speed = self.speed / self.move_speed
        angle = self.angle / np.pi
        angle_to_food = self._find_nearest(env.foods) / (np.pi * 2)
        age = self.age / env.steps
        return const, speed, angle, angle_to_food, age
    
    def step(self, env):
        self.energy -= 1
        self.age += 1

        # If the individual is out of food, don't do anything
        if self.energy <= 0:
            return
        
        # Activate brain
        inputs = self.normalized_inputs(env)
        actions = self.net.activate(inputs)

        # Add input to state
        speed = ((actions[0] + 1) / 2) * self.move_speed
        angle = self.angle + actions[1] * self.angular_speed

        new_x = self.x + speed * np.cos(angle)
        new_y = self.y + speed * np.sin(angle)

        # Wrap around angle
        if angle > np.pi:
            angle -= np.pi * 2
        elif angle < -np.pi:
            angle += np.pi * 2

        # Clamp position
        self.x = min(max(0, new_x), env.grid_size - 1)
        self.y = min(max(0, new_y), env.grid_size - 1)

        self.speed = speed
        self.angle = angle
        self.energy -= speed ** 2

    def _find_nearest(self, values):
        nodes = np.asarray(values)
        dist_2 = np.sum((nodes - (self.x, self.y)) ** 2, axis=1)

        if dist_2.size == 0:
            return 0

        nearest = np.argmin(dist_2)
        x, y = nodes[nearest]
        min_dist = np.sqrt(dist_2[nearest])

        # Return if the nearest entity is outside of view distance
        if min_dist > self.sight_range:
            return 0

        # Calculate angle
        x -= self.x
        y -= self.y
        angle = np.arctan2(y, x)

        return self.angle - angle
    
