import unittest

from src.mahjong.game import Game, Action

from tests.test_deck import test_deck


class GameTest(unittest.TestCase):
    def test_start_no_discards(self):
        game = Game()
        self.assertEqual(game.discard_pool, ())

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

    def test_discard(self):
        game = Game(test_deck)
        game.discard(0, 17)
        self.assertEqual(game.discard_pool, (17,))

    def test_can_chi_abc(self):
        game = Game(test_deck)
        game.discard(0, 5)
        self.assertEqual(game.discard_pool, (5,))
        self.assertSetEqual(
            game.allowed_actions(1),
            {Action.NOTHING, Action.CHI_A, Action.CHI_B, Action.CHI_C},
        )

    def test_can_nothing(self):
        game = Game(test_deck)
        game.discard(0, 17)
        self.assertEqual(game.discard_pool, (17,))
        self.assertSetEqual(
            game.allowed_actions(1),
            {Action.NOTHING},
        )

    def test_can_pon_kan(self):
        game = Game(test_deck)
        game.discard(0, 9)
        self.assertEqual(game.discard_pool, (9,))
        self.assertSetEqual(
            game.allowed_actions(1),
            {Action.NOTHING, Action.CHI_C, Action.PON, Action.OPEN_KAN},
        )
