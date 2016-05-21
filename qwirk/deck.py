import random
from queue import Queue
from threading import Thread, Timer

from qwirk.game import GameObj

class BadOptions(Exception):
    pass

class BadDeck(Exception):
    pass

class Deck():
    def __init__(self, settings):
        self.game = GameObj.game
        self.deck = []
        self.settings = settings
        for card in settings.rawDeck()['cards']:
            for c in range(0, card['count']):
                r = random.randint(0, 100)
                k = card.copy()
                k['priority'] += r
                del k['count']
                self.deck.append(k)
        random.shuffle(self.deck)

    def coerceRegisters(self, player, opcodes):
        """
        We're enforcing 3 things:
        1) Player has only changed unlocked cards
        2) Player has only used cards dealt to him
        3) Cards dealt have only been used once
        :param player: player object
        :param opcodes: list of opcodes to be assigned to player
        :return: valid list of opcodes
        """
        slicelen = min((self.settings.maxDamage-player.damage), len(player.opcodes))
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
        '''
        give cards to each player based on how many damage points he/she has
        receive card order from each player within a time limit
        :return:
        '''
        async = {}
        q = Queue(maxsize=0)
        for i in range(0, len(self.game.players)):
            for j in range(0, min(self.settings.handSize, self.settings.maxDamage - self.game.players[i].damage)):
                #As player sustains more and more damage, opcodes get locked
                op = self.deck.pop()
                self.game.players[i].opcodes[j] = op
            #After assigning cards, start a thread to receive input from player
            #This thread is meant to run longer than allowed just to make sure we never cut the player short
            t = Thread(target=self.game.io.receive, args=(q, self.game.players[i]))
            async[self.game.players[i].name] = {"q":q, "t":t, "recv": False}
            t.start()

        expire = Timer(60, q.put, {"src":"qtimer", "data":"expired"})
        expire.start()

        while False in [v['recv'] for k, v in async.items()]:
            resp = q.get(block=True)
            if resp['src'] == "qtimer":
                break #Out of time, all unrecv'd players will retain card order as dealt
            resp['src'].opcodes = self.coerceRegisters(resp['src'], resp['data'])
            async[resp['src'].name]['recv'] = True
        # Note that dealing puts opcodes in a player's opcode list. If they didn't respond
        # during the window above, they'll just retain the opcodes as dealt
        expire.cancel()
        print("All cards dealt")
        for i in range(0, len(self.game.players)):
            print("----===={}====----".format(self.game.players[i].name))
            print(self.game.players[i].opcodes)
