import os
import neat
import datetime
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

    # Run for up to n generations.
    winner = p.run(env.evaluate_genomes, 4)

    node_names = {
        -1: "constant",
        -2: "in speed",
        -3: "angle",
        -4: "angle to food",
        -5: "age",
        0: "out speed",
        1: "turn",
    }

    now = datetime.datetime.now()
    datestr = "%s%s%s_%s%s" % (now.year, now.month, now.day, now.hour, now.minute)

    os.mkdir("results/" + datestr)

    visualize.plot_stats(stats, ylog=False, view=True, filename=("results/" + datestr + "/avg_fitness_" + datestr + ".svg"))
    visualize.plot_species(stats, view=True, filename=("results/" + datestr + "/speciation_" + datestr + ".svg"))
    visualize.draw_net(config, winner, view=True, node_names=node_names, filename=("results/" + datestr +"/neural_net_" + datestr), fmt="png")

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
