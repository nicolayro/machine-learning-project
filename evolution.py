import os

import neat
import visualize

from environment import Environment

env = Environment()


# 2-input XOR inputs and expected outputs.
def eval_genomes(genomes, config):
    env.reset()
    for genome_id, genome in genomes:
        genome.fitness = 0
    for i in range(300):
        for (genome_id, genome), indiv in zip(genomes, env.individuals):
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            output = net.activate(indiv.inputs())
            indiv.execute_action(output)
            # genome.fitness = env.grid_size - (env.grid_size - indiv.pos[0])
            if indiv.pos[0] > 0.9 * env.grid_size:
                genome.fitness += 10

        if env.state % 50 == 49:
            env.render()
        # bad = [genome for (genome_id, genome) in genomes if genome.fitness is None]
        # print(bad)
    env.state += 1


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 1000)

    node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
