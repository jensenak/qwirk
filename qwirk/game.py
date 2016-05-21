from threading import Thread
from time import sleep
import re

class GameObj():
    game = None

class Game():
    def __init__(self):
        self.settings = None
        self.field = None
        self.players = None
        self.deck = None
        self.io = None
        self.round = 0

    def run(self):
        winner = False
        while not winner:
            self.round += 1
            print(self.round)
            self.deck.deal()
            self.play()
            winner = self.gameStatus()

        print("Bob wins!")
        return

    def play(self):
        # sort opcodes, perform in order with brief delay for interrupts
        for i in range(0, 5):
            cards = []
            for j in range(0, len(self.players)):
                cards.append({"player": self.players[j].name, "code": self.players[j].opcodes[i]})
            cards.sort(key=lambda card: card['code']['priority'])
            for k in cards:
                print("Player {} plays {}".format(k['player'], k['code']['name']))

        return

    def gameStatus(self):
        # evaluate living players, players who have reached all goals?
        return True

class IOModule():
    def notify(self, player, msg):
        print("NOTIFY: {}".format(msg))

    def broadcast(self, msg):
        print("BROADCAST: {}".format(msg))

    def receive(self, q, player):
        '''
        Receive user input
        This runs as a thread, and currently doesn't have a timeout of any kind.
        Risk of leaking threads.
        :param q:
        :param player:
        :return:
        '''
        # expire = Thread(target=sleep, args=(timeout,))
        # expire.start()
        # while expire.isAlive:
        print("Player {}".format(player.name))
        print([op['name'] for op in player.opcodes])
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

