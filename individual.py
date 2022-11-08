from food import Food
import numpy as np
import math


# Deprecated
class Individual:
    def __init__(self, pos, lifetime, sight):
        self.position = pos
        self.lifetime = lifetime
        self.sight = sight
        self.move_speed = 0.2

    # Represents an individual's action in one time step, given the circumstances
    def step(self, env):
        food = self.find_food(env)
        
        move_dir = (0.0, 0.0)

        if food:
            move_dir = (food.position[0] - self.position[0], food.position[1] - self.position[1])
            move_dir_len = distBetween(food.position, self.position)

            if move_dir_len > self.move_speed:
                move_dir = (move_dir[0] * self.move_speed / move_dir_len, move_dir[1] * self.move_speed / move_dir_len)
            
            if move_dir_len < (self.move_speed / 2):
                env.foods.remove(food)
                self.lifetime += food.nutrition
            
        else:
            angle = env.rand.random() * 2*math.pi
            move_dir = (math.cos(angle) * self.move_speed, math.sin(angle) * self.move_speed)
        
        # Move if not going out of bounds
        new_pos = (self.position[0] + move_dir[0], self.position[1] + move_dir[1])
        if new_pos[0] > 0 and new_pos[0] < env.grid_size and new_pos[1] > 0 and new_pos[1] < env.grid_size:
            self.position = new_pos

        self.lifetime -= 1

        if self.lifetime <= 0:
            env.individuals.remove(self)

    def find_food(self, env):
        min_dist = self.sight
        nearest_food = None

        for food in env.foods:
            dist = distBetween(self.position, food.pos)
            if dist < min_dist:
                min_dist = dist
                nearest_food = food
        
        return nearest_food

def distBetween(a, b) -> float:
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
