class Game():
    def __init__(self, room, map, players, deck):
        self.room = room
        self.map = map
        self.players = players
        self.deck = deck

    def run(self):
        