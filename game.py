from threading import Thread
from queue import Queue
from time import sleep
import field, player, deck

#GLOBAL GAME OBJECT
game = ""

class Game():
    def __init__(self, field, players, deck, ioModule):
        self.field = field
        self.players = players
        self.deck = deck
        self.io = ioModule
        self.maxDamage = 8
x
    def run(self):
        winner = False
        while not winner:
            self.deal()
            self.play()
            winner = self.gameStatus()



    def play(self):
        # sort opcodes, perform in order with brief delay for interrupts
        pass

    def gameStatus(self):
        # evaluate living players, players who have reached all goals?
        return True

    def qTimer(self, q, timeout):
        sleep(timeout)
        q.put({"src":"qtimer", "data":"done"})

class IOModule():
    def notify(self, player, msg):
        print("NOTIFY: {}".format(msg))

    def broadcast(self, msg):
        print("BROADCAST: {}".format(msg))

    def receive(self, q, player):
        for i in range(0, 15):
            sleep(1)
        q.put({"src":player, "data":"done"})
        return

if __name__ == "__main__":
    game = Game(field.Field('assets/maps/example.json'),
                [player.Player('1234-asdf', 'Bob')],
                deck.Deck('assets/decks/deck.json'),
                IOModule())
    game.run()