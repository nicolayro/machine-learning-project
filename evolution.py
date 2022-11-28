import os
import sys
import neat
import datetime
import pickle
import random
import visualize
import environment

generations = 100
seed = 42
random.seed(seed)
env = environment.Environment(seed)

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)
    config.pop_size = env.pop_size

    if '-l' in sys.argv:
        handle_duel(config)
        return
 
    now = datetime.datetime.now()
    datestr = "%s%s%s_%s%s" % (now.year, now.month, now.day, now.hour, now.minute)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100, filename_prefix="results/" + datestr + "/neat-checkpoint"))

    # Run for up to n generations.
    winner = p.run(env.evaluate_genomes, generations)

    node_names = {
        -1: "constant",
        -2: "vision 0",
        -3: "vision 1",
        -4: "vision 2",
        -5: "vision 3",
        -6: "vision 4",
        0: "out speed",
        1: "turn",
    }

    os.mkdir("results/" + datestr)

    visualize.plot_stats(stats, ylog=False, view=True, filename=("results/" + datestr + "/avg_fitness_" + datestr + ".svg"))
    visualize.draw_net(config, winner, view=True, node_names=node_names, filename=("results/" + datestr +"/neural_net_" + datestr), fmt="png")

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    best_late_fitness = 0
    best_late_g = None

    for g in stats.most_fit_genomes[-30:]:
        if g.fitness > best_late_fitness:
            best_late_fitness = g.fitness
            best_late_g = g

    if '-s' in sys.argv:
        with open("winner_" + sys.argv[2] + ".pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

def handle_duel(config):
    winner1 = None
    winner2 = None

    with open("winner_" + sys.argv[2] + ".pkl", "rb") as f:
        winner1 = pickle.load(f)
        
    with open("winner_" + sys.argv[3] + ".pkl", "rb") as f:
        winner2 = pickle.load(f)
    
    env.handle_duel(winner1, winner2, config, 100)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
