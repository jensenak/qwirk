import json

class BoardInterrupt(Exception):
    pass

class Field():
    def __init__(self, file):
        with open(file, 'r') as f:
            self.field = json.load(f)

    def get(self, x, y):
        tmp = self.field['defs'][self.field['map'][x][y]]
        if 'parent' in tmp:
            return extend(tmp['parent'].copy(), tmp)
        return tmp

    def enterSpace(self, dir, x, y):
        '''
        Can the current space be entered?
        Are there immediate board effects?
        :param dir: string direction the bot is moving (n, e, s, w)
        :param x: numerical space coord
        :param y: numerical space coord
        :return: bool if entering is permitted, or exception with immediate effect
        '''
        if dir not in self.get(x, y)['enter']:
            return False
        if "event_timing" in self.get(x, y) and self.get(x, y)["event_timing"] == "now":
            raise BoardInterrupt(x, y)
        #Nothing else happened, must be okay.
        return True

    def boardEffect(self, player):
        x, y = player.location
        square = self.get(x, y)
        if 'damage' in square:
            player.damage += square['damage']
        if 'move' in square:
            player.move(f=square['speed'], h=square['dir'])

def extend(a, b):
    '''
    extend dictionary a with dictionary b
    probably a native way to do this, but can't find until I have internet
    :param a: dict
    :param b: dict
    :return: dict
    '''
    for k, v in b.items():
        if k in a and isinstance(v, dict):
            extend(a[k], b[k])
        else:
            a[k] = b[k]