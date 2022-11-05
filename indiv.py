import params
import numpy as np

# Individual in the environment
class Indiv:

    def __init__(self, pos, angle, speed):
        # Inputs
        self.pos = pos
        self.angle = angle
        self.speed = speed

    def inputs(self):
        #return [(self.pos[0], self.pos[1], self.angle, self.age, np.random.random(), self.always)]
        return self.pos[0], self.pos[1], self.angle

    def execute_action(self, action):
        new_pos = (self.pos[0] + action[0], self.pos[1] + action[1])
        #self.age += 1
        #s = action[0]
        #a = self.angle + (action[1] * np.pi)
        # Add the vectors to the position
        #new_pos = (self.pos[0] + s * np.sin(a), self.pos[1] + s * np.cos(a))
        if new_pos[0] > 0 and new_pos[0] < params.GRID_SIZE and new_pos[1] > 0 and new_pos[1] < params.GRID_SIZE:
            self.pos = new_pos

    def move(self, movement):
        pass
