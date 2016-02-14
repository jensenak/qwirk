from game import GameObj
import field

class InvalidMovement(Exception):
    pass

class Player():
    '''
    Player is a class to keep track of the robot and its status, as well as the players' "cards" or opcodes.
    '''
    def __init__(self, wsid, name):
        self.game = GameObj.game
        self.wsid = wsid
        self.name = name
        self.opcodes = [0 for i in range(self.game.deck.handSize)]
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
        try:
            self.location = pathFinder(self.location, x, y)
        except field.BoardInterrupt as e:
            self.location = e.args
            self.game.field.boardEffect(self)

def pathFinder(start, x, y):
    '''
    pathFinder is a common utility for determining if a space can be entered.
    It handles pushing, pushing with obstacles, and immediate effect board elements
    :param start: tuple of x, y start position
    :param x: delta x
    :param y: delta y
    :return: tuple final position
    '''
    x0 = start[0]
    y0 = start[1]
    if x and y:
        raise InvalidMovement("Cannot move in both X and Y")
    if x:
        for xi in range(x0, x, x/abs(x)):
            if not self.game.field.enterSpace(xi, y0):
                return (xi, y0)
        return (x, y0)
    for yi in range(y0, y, y/abs(y)):
        if not self.game.field.enterSpace(x0, yi):
            return (x0, yi)
    return (x0, y)

def xyTranslate(f, s, h):
    '''
    Take forward, sideways movement and convert to map x, y
    :param f: numerical forward
    :param s: numerical sideways
    :param h: letter heading (n, e, s, w)
    :return: tuple (x, y) of map absolute movement
    '''
    if h == "n":
        return (s, -f) #North means forward = -y right = +x
    if h == "e":
        return (f, s) #East means forward = +x right = +y
    if h == "s":
        return (-s, f) #South means forward = +y right = -x
    if h == "w":
        return (-f, -s) #West means forward = -x right = -y
    raise InvalidMovement("Heading must be 0 - 3")
