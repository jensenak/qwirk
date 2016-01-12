class Field():
    def __init__(self, x, y, features):
        self.map = [[0 for i in range(x)] for j in range(y)]
        self.features = []
        for feat in features:
            self.features[len(self.features)] = feat['props']
            self.map[feat['x']][feat['y']] = len(self.features)

    def enterSpace(self, x, y):
        return self.map[x][y]