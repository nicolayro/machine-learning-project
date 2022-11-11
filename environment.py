import numpy as np
import neat

from indiv import Indiv
from renderer import Renderer


class Environment:
    grid_size   = 80    # Size of the world
    pop_size    = 60    # Initial population size
    num_food    = 100   # Initial amount of food
    nutrition   = 200   # Food nutrition
    steps       = 400   # Number of time steps per generation
    grass_nutrition = 2 # Grass nutrition from eating
    grass_factor = 4    # How much tile value decreases when eating

    agents = []
    foods = []
    grass = []

    def __init__(self, seed):
        self.rand = np.random.default_rng(seed)
        self.state = 0
        self.renderer = Renderer(self.grid_size)

    def evaluate_genomes(self, genomes, config):
        self.state += 1
        self.agents = []
        self.foods = []
        # Initialize
        for genome_id, genome in genomes:
            # Create a brain
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            # Create an agent and connect the brain
            x = self.rand.random() * (self.grid_size - 1) + 0.5
            y = self.rand.random() * (self.grid_size - 1) + 0.5
            a = self.rand.random() * 2 * np.pi
            agent = Indiv(x, y, a, net)
            self.agents.append(agent)

        # Simulate
        self.foods = self.rand.random((self.num_food, 2)) * (self.grid_size - 4) + 2    # Spawn food
        self.grass = self.rand.random((self.grid_size, self.grid_size)) * 100 + 30      # Spawn grass
        for i in range(self.steps):
            for agent in self.agents:
                # Agent acts
                agent.step(self)

                # Check food
                new_foods = np.delete(self.foods, np.where(
                    (abs(self.foods[:, 0] - agent.x) < 0.5) &
                    (abs(self.foods[:, 1] - agent.y) < 0.5))[0], axis=0)
                agent.energy += self.nutrition * (len(self.foods) - len(new_foods))
                self.foods = new_foods

            # Render world to screen
            if self.state % 50 == 0:
                self.renderer.render(self)

        # Evaluate
        for (genome_id, genome), agent in zip(genomes, self.agents):
            genome.fitness = agent.energy

    def get_normalized_nutrition(self, agent: Indiv) -> float:
        x = int(round(agent.x))
        y = int(round(agent.y))

        return self.grass[x][y] / 130

    def eat_grass(self, agent: Indiv) -> float:
        x = int(round(agent.x))
        y = int(round(agent.y))

        tile_value = self.grass[x][y]
        eat_amount = self.grass_nutrition * self.grass_factor

        if tile_value >= eat_amount:
            self.grass[x][y] -= eat_amount
            return self.grass_nutrition
        else:
            value = self.grass[x][y]
            self.grass[x][y] = 0
            return value / self.grass_factor