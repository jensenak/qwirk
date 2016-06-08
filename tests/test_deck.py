import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from qwirk.deck import Deck, BadOptions, BadDeck
import unittest

class SharedSettings:
    def __init__(self, handsize, cards):
        self.handSize = handsize
        self.cards = cards
        self.maxDamage = 8

    def rawDeck(self):
        return self.cards

class MockPlayer:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.opcodes = []
        self.damage = 0

class TestConstructor(unittest.TestCase):
    def setUp(self):
        self.cards = {
            "valid": {
                "name":"movement only",
                "cards":[
                    {"name":"forward one","type":"move", "dir":"f", "speed": 1, "priority":500, "count":3},
                    {"name":"right one","type":"move", "dir":"s", "speed": 1, "priority":300, "count":1},
                    {"name":"right turn","type":"move", "dir":"h", "speed": 1, "priority":800, "count":2}
                ]
            },
            "invalid": {
                "name":6,
                "coords":{"nope":True}
            }
        }

        self.hand = {"valid": 7, "invalid1": 4, "invalid2": 11}

    def test_handsize(self):
        self.assertTrue(Deck(SharedSettings(self.hand['valid'], self.cards['valid'])))
        with self.assertRaises(BadOptions):
            Deck(SharedSettings(self.hand['invalid1'], self.cards['valid']))
        with self.assertRaises(BadOptions):
            Deck(SharedSettings(self.hand['invalid2'], self.cards['valid']))

    def test_deck(self):
        self.assertTrue(Deck(SharedSettings(self.hand['valid'], self.cards['valid'])))
        with self.assertRaises(BadDeck):
            Deck(SharedSettings(self.hand['valid'], self.cards['invalid']))

class TestCoercion(unittest.TestCase):
    def setUp(self):
        self.validPlayer = MockPlayer('aaaa', 'Bob')
        self.validPlayer.opcodes = ['a','b','c','d','e','f','g']
        self.invalidPlayer = {"name":"Bill", "opcodes":['1','2','3','4']}
        self.codes = {"valid": ['f','a','d','e','g'],
                      "locked": ['e', 'f', 'g'],
                      "invalid": [1, 2, 3, 4]}
        self.deck = Deck(SharedSettings(7, {"cards":[]}))

    def test_opcodes(self):
        self.deck.coerceRegisters(self.validPlayer, self.codes['valid'])
        self.assertEqual(self.validPlayer.opcodes, ['f', 'a', 'd', 'e', 'g', 'b', 'c'])

if __name__ == "__main__":
    unittest.main()
