from qwirk import common


class all:
    def __init__(self, deckFile, fieldFile):
        self.deckFile = deckFile
        self.fieldFile = fieldFile
        self.handSize = 7
        self.maxDamage = 8

    def rawField(self):
        return common.jsonFromFile(self.fieldFile)

    def rawDeck(self):
        return common.jsonFromFile(self.deckFile)