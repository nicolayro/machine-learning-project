import params

# Individual in the environment
class Indiv:

    def __init__(self, pos, angle, speed):
        # Inputs
        self.pos = pos
        self.angle = angle
        self.speed = speed
        self.id = 0

    def inputs(self):
        return [self.pos]

    def execute_action(self, action):
        new_pos = (self.pos[0] + action[0], self.pos[1] + action[1])
        if new_pos[0] > 0 and new_pos[0] < params.GRID_SIZE and new_pos[1] > 0 and new_pos[1] < params.GRID_SIZE:
            self.pos = new_pos


        return
        if action == "rotate_left":
            print("rotating left")
        elif action == "rotate_right":
            print("rotating right")
        elif action == "move forward":
            print("moving forward")
        elif action == "move random":
            print("moving randomly")
        else:
            raise RuntimeError(f"Unhandled action: {action}")

    def move(self, movement):
        pass
