import numpy as np
import neat

from agent import Agent
from renderer import Renderer
from indiv import Indiv


class Environment:
    grid_size   = 128   # Size of the world
    pop_size    = 240   # Initial population size
    num_food    = 320   # Initial amount of food
    nutrition   = 200   # Food nutrition
    steps       = 300   # Number of time steps per generation

    agents = []
    foods = []

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
            agent = Agent(x, y, a, net)
            self.agents.append(agent)

        # Simulate
        self.foods = self.rand.random((self.num_food, 2)) * (self.grid_size - 4) + 2  # Spawn food
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
            if self.state % 50 == 0 or self.state == 1:
                self.renderer.render(self)

        # Evaluate
        for (genome_id, genome), agent in zip(genomes, self.agents):
            genome.fitness = agent.energy


