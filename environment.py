import numpy as np
import neat
import copy

from indiv import Indiv
from renderer import Renderer


class Environment:
    grid_size   = 64    # Size of the world
    pop_size    = 60    # Initial population size
    num_food    = 80    # Initial amount of food
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
            a = self.rand.random() * 2 * np.pi - np.pi
            agent = Indiv(x, y, a, net)
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
            #if self.state % 100 == 0:
            self.renderer.render(self)

        # Evaluate
        for (genome_id, genome), agent in zip(genomes, self.agents):
            genome.fitness = agent.energy

    def handle_duel(self, genome1, genome2, config, runs):
        genome1_values = 0
        genome2_values = 0
        genome1_max = 0
        genome2_max = 0

        for i in range(runs):
            mean1, max1, mean2, max2 = self.simulate_duel(genome1, genome2, config)
            print("Run " + str(i))
            genome1_values += mean1
            genome2_values += mean2

            if max1 > genome1_max:
                genome1_max = max1
            if max2 > genome2_max:
                genome2_max = max2
        
        print("FINAL RESULT\n---------------------")
        print("Genome 1:\tMean: " + str(genome1_values / runs) + "\tMax: " + str(genome1_max))
        print("Genome 2:\tMean: " + str(genome2_values / runs) + "\tMax: " + str(genome2_max))

    def simulate_duel(self, genome1, genome2, config):
        self.agents = []
        self.foods = []

        for i in range(30):
            genome = copy.deepcopy(genome1)
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            
            x = self.rand.random() * (self.grid_size - 1) + 0.5
            y = self.rand.random() * (self.grid_size - 1) + 0.5
            a = self.rand.random() * 2 * np.pi - np.pi
            agent = Indiv(x, y, a, net)
            self.agents.append(agent)
        
        for i in range(30):
            genome = copy.deepcopy(genome2)
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome2, config)
            
            x = self.rand.random() * (self.grid_size - 1) + 0.5
            y = self.rand.random() * (self.grid_size - 1) + 0.5
            a = self.rand.random() * 2 * np.pi - np.pi
            agent = Indiv(x, y, a, net)
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

        genome1_score = 0
        genome1_max = 0
        for i in range(30):
            genome1_score += self.agents[i].energy
            if self.agents[i].energy > genome1_max:
                genome1_max = self.agents[i].energy
        genome1_score /= 30

        genome2_score = 0
        genome2_max = 0
        for i in range(30, 60):
            genome2_score += self.agents[i].energy
            if self.agents[i].energy > genome2_max:
                genome2_max = self.agents[i].energy
        genome2_score /= 30

        return genome1_score, genome1_max, genome2_score, genome2_max

