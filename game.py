from threading import Thread
from time import sleep
import re

class GameObj():
    game = None

class Game():
    def __init__(self):
        self.field = None
        self.players = None
        self.deck = None
        self.io = None
        self.maxDamage = 8

    def run(self):
        winner = False
        while not winner:
            self.deck.deal()
            self.play()
            winner = self.gameStatus()

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

    def receive(self, q, player, timeout):
        expire = Thread(target=sleep, args=(timeout,))
        expire.start()
        while expire.isAlive:
            print("Player {}".format(player.name))
            print([op.name for op in player.opcodes])
            nums = input('Type comma separated numbers for desired card order: ')
        choices = map(int, re.findall('\d', nums))
        final = []
        try:
            for n in choices:
                final.append(player.opcodes[n])
        except Exception:
            final = player.opcodes # Take that ya fart face... throwing exceptions... how rude

        q.put({"src":player, "data":final})
        return

