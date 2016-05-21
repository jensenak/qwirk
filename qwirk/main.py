import field
import game
import player
import settings

from qwirk import deck

if __name__ == "__main__":
    g = game.Game()
    game.GameObj.game = g
    g.settings = settings.all('assets/decks/deck.json', 'assets/maps/example.json')
    g.field = field.Field(g.settings)
    g.deck = deck.Deck(g.settings)
    g.players = [player.Player('0000-aaaa', 'Bob')]
    g.io = game.IOModule()
    g.run()