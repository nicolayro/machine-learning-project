import os
import neat
import random

import visualize
import environment

# Seeding
seed = 42
random.seed(seed)
env = environment.Environment(seed)


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    config.pop_size = env.pop_size

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100, filename_prefix="results/neat-checkpoint"))

    # Run for up to 400 generations.
    winner = p.run(env.evaluate_genomes, 100)

    print('\nBest genome:\n{!s}'.format(winner))

    node_names = {
        -1: "const",
        -2: "random",
        -3: "x",
        -4: "y",
        -5: 'angle',
        -6: 'age',
        -7: "angle_food",
        -8: "dist_food",
        0: "forward",
        1: "turn left",
        2: "turn right"
    }
    # Display the winning genome.
    visualize.draw_net(config, winner, True, node_names=node_names, filename="results/brain")
    visualize.plot_stats(stats, ylog=False, view=True, filename="results/avg_fitness.svg")
    visualize.plot_species(stats, view=True, filename="results/speciation.svg")


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
