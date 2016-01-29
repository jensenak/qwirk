import

class Field():
    def __init__(self, file):
        self.readMap()

    def readMap(self, file):
        with open(file, 'r') as f:
            map = json.load(f)
            self.map = [[map['fill'] for i in range(map['height'])] for j in range(map['width'])]
            self.features = []
            for feat in map.features:
                self.features[len(self.features)] = feat['props']
                self.map[feat['x']][feat['y']] = len(self.features)
        return

    def enterSpace(self, x, y):
        return self.map[x][y]