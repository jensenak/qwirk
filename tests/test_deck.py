import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from qwirk.deck import Deck, BadOptions, BadDeck
import unittest

class testSettings:
    def __init__(self, handsize, cards):
        self.handSize = handsize
        self.cards = cards

    def rawDeck(self):
        return self.cards

validCards1 = {
    "name":"movement only",
    "cards":[
        {"name":"forward one","type":"move", "dir":"f", "speed": 1, "priority":500, "count":3},
        {"name":"forward two","type":"move", "dir":"f", "speed": 2, "priority":300, "count":1}
    ]
}

validCards2 = {
    "name":"movement only",
    "cards":[
        {"name":"forward one","type":"move", "dir":"f", "speed": 1, "priority":500, "count":3},
        {"name":"right one","type":"move", "dir":"s", "speed": 1, "priority":300, "count":1},
        {"name":"right turn","type":"move", "dir":"h", "speed": 1, "priority":800, "count":2}
    ]
}

invalidCards = {
    "name":6,
    "cords":{"nope":True}
}

validHand1 = 7
validHand2 = 10
invalidHand1 = 4
invalidHand2 = 11

class TestConstructor(unittest.TestCase):
    def test_handsize(self):
        self.assertTrue(Deck(testSettings(validHand1, validCards1)))
        self.assertTrue(Deck(testSettings(validHand2, validCards1)))
        with self.assertRaises(BadOptions):
            Deck(testSettings(invalidHand1, validCards1))
        with self.assertRaises(BadOptions):
            Deck(testSettings(invalidHand2, validCards1))

    def test_deck(self):
        self.assertTrue(Deck(testSettings(validHand1, validCards1)))
        self.assertTrue(Deck(testSettings(validHand1, validCards2)))
        with self.assertRaises(BadDeck):
            Deck(testSettings(validHand1, invalidCards))

if __name__ == "__main__":
    unittest.main()
