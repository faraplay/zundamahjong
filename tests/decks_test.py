import unittest

from tests.decks import *


class DeckTest(unittest.TestCase):
    def test_deck_sizes(self):
        for test_deck in [test_deck1, test_deck2, test_deck3, test_deck4]:
            self.assertCountEqual(test_deck, deck)
