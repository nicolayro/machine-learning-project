import params
import numpy as np

index_to_action = ['MOVE_FORWARD', 'TURN_LEFT', 'TURN_RIGHT']


# Individual in the environment
class Indiv:
    # Some initial values
    max_energy = params.EPISODE_LENGTH
    sight_range = params.SIGHT_RANGE
    speed = params.SPEED
    angular_speed = params.ANGULAR_SPEED

    def __init__(self, pos, angle):
        # Inputs
        self.pos = pos
        self.angle = angle

        self.age = 0
        self.energy = self.max_energy

    def inputs(self, env):
        # Normalize values
        # pos_x = self._normalize(self.pos[0], params.GRID_SIZE)
        # pos_y = self._normalize(self.pos[1], params.GRID_SIZE)
        angle = self._normalize(self.angle, 2 * np.pi)
        # age = self._normalize(self.age, params.EPISODE_LENGTH)
        energy = self._normalize(self.energy, self.max_energy)
        random = np.random.random()

        # Relative position of the nearest food
        food_dist, food_angle = self._find_nearest(env.foods, self.sight_range)
        indiv_dist, indiv_angle = self._find_nearest(env.individuals, self.sight_range)

        food_angle = self._normalize(food_angle, 2 * np.pi)
        food_dist = self._normalize(food_dist, self.sight_range)
        # indiv_dist = self._normalize(indiv_dist, 2 * np.pi)
        # indiv_angle = self._normalize(indiv_angle, self.sight_range)

        return angle, energy, random, 1, food_angle, food_dist
        # return pos_x, pos_y, angle, age, energy, random, 1, food_angle, food_dist, indiv_angle, indiv_dist

    def execute_actions(self, outputs):
        self.energy -= 1
        self.age += 1

        # If the individual is out of food, don't do anything
        if self.energy <= 0:
            return

        # Handle actions
        actions = []
        for index, output in enumerate(outputs):
            if output > np.random.random():
                actions.append(index_to_action[index])
        self._execute_actions(actions)

    def _execute_actions(self, actions):
        speed = 0
        angle = self.angle

        # Handle actions
        if 'MOVE_FORWARD' in actions:
            speed = self.speed

        if 'TURN_LEFT' in actions:
            angle -= self.angular_speed

        if 'TURN_RIGHT' in actions:
            angle += self.angular_speed

        # Calculate new position
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
