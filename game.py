class Game():
    def __init__(self, room, map, players, deck):
        self.room = room
        self.map = map
        self.players = players
        self.deck = deck

    def run(self):
        winner = False
        while not winner:
            self.deal()
            self.play()
            winner = self.gameStatus()

    def deal(self):
        #distribute opcodes
        #start timer
        #when all opcodes declared || timer expires, proceed
        pass

    def play(self):
        # sort opcodes, perform in order with brief delay for interrupts
        pass

    def gameStatus(self):
        # evaluate living players, players who have reached all goals?
        return True
