import unittest

from src.mahjong.game import Game

from tests.test_deck import test_deck


class GameTest(unittest.TestCase):
    def test_start_game(self):
        game = Game()
        self.assertTrue(True)

    def test_fixed_deck(self):
        game = Game(test_deck)
        self.assertTrue(True)

    def test_fixed_deck_start_hands(self):
        game = Game(test_deck)
        self.assertEqual(
            game.get_hand(0), (1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21, 21, 21)
        )
        self.assertEqual(game.get_hand(1), (1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21))
        self.assertEqual(
            game.get_hand(2), (11, 11, 11, 11, 13, 13, 13, 13, 15, 15, 15, 15, 17)
        )
        self.assertEqual(
            game.get_hand(3), (12, 12, 12, 12, 14, 14, 14, 14, 16, 16, 16, 16, 17)
        )
