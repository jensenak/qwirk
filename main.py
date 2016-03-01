import game, field, player, deck

if __name__ == "__main__":
    g = game.Game()
    game.GameObj.game = g
    g.field = field.Field('assets/maps/example.json')
    g.deck = deck.Deck('assets/decks/deck.json')
    g.players = [player.Player('0000-aaaa', 'Bob')]
    g.io = game.IOModule()
    g.run()