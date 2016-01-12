class Opcode():
    def __init__(self, m, o):
        self.movement = {}
        self.owner = o


class Deck():
    def __init__(self, opcodes=None):
        if opcodes:
            self.opcodes = opcodes
        self.opcodes = []
