import numpy as np

# Individual in the environment
class Indiv:
    start_energy        = 300   # Initial energy 
    energy              = start_energy
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
        age = self.age / env.steps
        energy = self.energy / self.start_energy
        vision = self._get_normalized_vision(env.foods)
        return const, age, energy, vision[0], vision[1], vision[2], vision[3], vision[4]
    
    def step(self, env):
        self.age += 1

        # If the individual is out of food, don't do anything
        if self.energy <= 0:
            self.energy = 0
            return
        
        # Activate brain
        inputs = self.normalized_inputs(env)
        actions = self.net.activate(inputs)

        # Add input to state
        speed = actions[0] * self.move_speed
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

        self.energy -= 1
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
    
    def _get_normalized_vision(self, values):
        range_squared = self.sight_range ** 2
        squared_min_dist = [range_squared, range_squared, range_squared, range_squared, range_squared]

        if values.size == 0:
            return [0, 0, 0, 0, 0]

        for value in values:
            angle = self.angle - np.arctan2(value[1] - self.y, value[0] - self.x)

            if abs(angle) < ((2 * np.pi) / 3):
                dist_squared = (value[0] - self.x) ** 2 + (value[1] - self.y) ** 2

                if dist_squared < range_squared:
                    if angle < (-np.pi / 4):
                        if dist_squared < squared_min_dist[0]:
                            squared_min_dist[0] = dist_squared 
                    elif angle < (-np.pi / 24):
                        if dist_squared < squared_min_dist[1]:
                            squared_min_dist[1] = dist_squared 
                    elif angle < (np.pi / 24):
                        if dist_squared < squared_min_dist[2]:
                            squared_min_dist[2] = dist_squared 
                    elif angle < (np.pi / 4):
                        if dist_squared < squared_min_dist[3]:
                            squared_min_dist[3] = dist_squared 
                    else:
                        if dist_squared < squared_min_dist[4]:
                            squared_min_dist[4] = dist_squared
        
        impulses = [0, 0, 0, 0, 0]

        for i in range(5):
            impulses[i] = (self.sight_range - np.sqrt(squared_min_dist[i])) / self.sight_range
        
        return impulses