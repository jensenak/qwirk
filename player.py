field = {'enterSpace': lambda x, y: 0}

class InvalidMovement(Exception):
    pass

class Player():
    '''
    Player is a class to keep track of the robot and its status, as well as the players' "cards" or opcodes.
    '''
    def __init__(self, wsid, name):
        self.wsid = wsid
        self.name = name
        self.opcodes = []
        self.registers = 5
        self.damage = 0
        self.location = (0, 0)
        self.heading = 0
        self.weapon = 'standard'
        return

    def move(self, f=0, s=0, x=0, y=0, r=0):
        if r:
            self.heading = (self.heading + r) % 4
            return 0
        if f or s:
            x, y = xyTranslate(f, s, self.heading)
        self.location = pathFinder(self.location, x, y)

def pathFinder(start, x, y):
    x0 = start[0]
    y0 = start[1]
    if x and y:
        raise InvalidMovement("Cannot move in both X and Y")
    if x:
        for xi in range(x0, x, x/abs(x)):
            if field.enterSpace(xi, y0) != 0:
                return (xi, y0)
        return (x, y0)
    for yi in range(y0, y, y/abs(y)):
        if field.enterSpace(x0, yi) != 0:
            return (x0, yi)
    return (x0, y)

def xyTranslate(f, s, h):
    if h == 0:
        return (-f, s)
    if h == 1:
        return (s, f)
    if h == 2:
        return (f, -s)
    if h == 3:
        return (-s, -f)
    raise InvalidMovement("Heading must be 0 - 3")
