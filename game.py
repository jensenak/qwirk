import field, player, deck

#GLOBAL GAME OBJECT
game = ""

class Game():
    def __init__(self, field, players, deck, ioModule):
        self.field = field
        self.players = players
        self.deck = deck
        self.io = ioModule

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

class IOModule():
    def notify(self, player, msg):
        print("NOTIFY: {}".format(msg))

    def broadcast(self, msg):
        print("BROADCAST: {}".format(msg))

if __name__ == "__main__":
    game = Game(field.Field('assets/maps/example.json'),
                [player.Player('1234-asdf', 'Bob')],
                deck.Deck('assets/decks/deck.json'),
                IOModule())
    game.run()