import json
import random

class Deck():
    def __init__(self, file):
        self.deck = []
        with open(file, 'r') as f:
            d = json.load(f)
        for card in d['deck']:
            for c in range(0, card['count']):
                r = random.randint(0, 100)
                k = card.copy()
                k['priority'] += r
                self.deck.append(k)

    def shuffle(self, iter):
        for i in range(0, len(self.deck)*iter):
            r = random.randint(0, len(self.deck)-1)
            k = self.deck.pop(r)
            self.deck.append(k)