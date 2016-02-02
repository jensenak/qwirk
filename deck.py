from queue import Queue
from threading import Thread
from time import sleep
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

    def coerceRegisters(self, player, opcodes):
        '''
        We're enforcing 3 things:
        1) Player has only changed unlocked cards
        2) Player has only used cards dealt to him
        3) Cards dealt have only been used once
        :param player: player object
        :param opcodes: list of opcodes to be assigned to player
        :return: valid list of opcodes
        '''
        slicelen = min((game.maxDamage-player.damage), len(player.opcodes))
        avail = player.opcodes[:slicelen] # copy unlocked opcodes
        newops = []
        for i in opcodes:
            try:
                # Remove the opcode from the available list and append it to the valid one
                avail.remove(i)
                newops.append(i)
            except ValueError:
                # Value error raised when opcode not in available list
                newops.append(avail.pop) # Player shouldn't have cheated... now everything's messed up
        return newops

    def deal(self):
        async = {}
        q = Queue(maxsize=0)
        for j in range(0, len(game.players)):
            for j in range(0, min(self.handSize, game.maxDamage - game.players[i].damage)):
                #As player sustains more and more damage, opcodes get locked
                op = self.deck.pop()
                game.players[j].opcodes[j] = op
            #After assigning cards, start a thread to receive input from player
            t = Thread(target=game.io.receive, args=(q, game.players[j], 300))
            async[game.players[j].name] = {"q":q, "t":t}
            t.start()

        expire = Thread(target=qTimer, args=(q, 90))
        expire.start()
        while True:
            resp = q.get(block=True)
            if resp['src'] == "qtimer":
                break #Out of time, all unrecv'd players will retain card order as dealt
            resp['src'].opcodes = self.validate(resp['src'], resp['data'])
            recvd.append(resp['src'])
        # Note that dealing puts opcodes in a player's opcode list. If they didn't respond
        # during the window above, they'll just retain the opcodes as dealt

    def qTimer(self, q, timeout):
        sleep(timeout)
        q.put({"src":"qtimer", "data":"done"})