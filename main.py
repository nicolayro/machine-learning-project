from environment import Environment

if __name__ == '__main__':
    env = Environment(grid_size=40, fps=2, num_of_ind=1, num_of_food=50)
    env.render()
