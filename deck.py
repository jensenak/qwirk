from queue import Queue
from threading import Thread
import json
import random

from game import game

class Deck():
    def __init__(self, file):
        self.deck = []
        self.handSize = 7
        with open(file, 'r') as f:
            d = json.load(f)
        for card in d['deck']:
            for c in range(0, card['count']):
                r = random.randint(0, 100)
                k = card.copy()
                k['priority'] += r
                self.deck.append(k)
        random.shuffle(self.deck)

    def validateRegisters(self, player, opcodes):

    def deal(self):
        for j in range(0, len(game.players)):
            for j in range(0, min(self.handSize, game.maxDamage - game.players[i]['damage'])):
                #As player sustains more and more damage, opcodes get locked
                op = self.deck.pop()
                game.players[j]['opcodes'][j] = op

        async = {}
        q = Queue(maxsize=0)
        for j in range(0, len(self.players)):
            t = Thread(target=self.io.receive, args=(q, self.players[j]))
            async[self.players[j]['name']] = {"q":q, "t":t}
            t.start()

        recvd = []
        while True:
            resp = q.get(block=True)
            if resp['src'] == "qtimer":
                break
            resp['src']['opcodes'] = self.deck.validate(resp['src'], resp['data'])
            recvd.append(resp['src'])

        for j in range(0, len(self.players)):
            if self.players[j] not in recvd:
                self.players[j]['opcodes'] = self.deck.validate(self.players[j], "")