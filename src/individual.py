class Individual:
    def __init__(self, lifetime, sight):
        self.lifetime = lifetime
        self.sight = sight

    def step(self, pos, env):
        pass

    def get_visible_area(self, pos, env):
        # Returns coordinates for a circle
        circle = []
        X = int(self.sight + 1)
        r = int(self.sight + 1)
        for x in range(-X, X + 1):
            Y = int((r * r - x * x) ** 0.5)
            if Y == 0:
                continue
            if Y > self.sight:
                Y = self.sight
            for y in range(-Y, Y + 1):
                circle.append([x + self.sight, y + self.sight])
        return circle
