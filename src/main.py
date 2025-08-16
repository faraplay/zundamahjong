from mahjong import Game, Deck

if __name__ == "__main__":
    game = Game(Deck.shuffled_deck())
    game.display_info()
