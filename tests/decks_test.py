import unittest

from src.mahjong.deck import four_player_deck

from tests.decks import *


class DeckTest(unittest.TestCase):
    def test_deck_sizes(self) -> None:
        for test_deck in [test_deck1, test_deck2, test_deck3, test_deck4, test_deck5]:
            self.assertCountEqual(test_deck, four_player_deck)
