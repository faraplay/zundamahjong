import unittest

from src.mahjong.action import Action, ActionType
from src.mahjong.game import Game

from tests.test_deck import test_deck, test_deck2


class AllowedActionTest(unittest.TestCase):
    def test_play_default_actions(self):
        game = Game(test_deck)
        self.assertEqual(
            game.allowed_actions(0).default, Action(ActionType.DISCARD, 21)
        )
        self.assertEqual(game.allowed_actions(1).default, Action(ActionType.NOTHING))
        self.assertEqual(game.allowed_actions(2).default, Action(ActionType.NOTHING))
        self.assertEqual(game.allowed_actions(3).default, Action(ActionType.NOTHING))

    def test_discarded_default_actions(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 9))
        self.assertEqual(game.allowed_actions(0).default, Action(ActionType.NOTHING))
        self.assertEqual(game.allowed_actions(1).default, Action(ActionType.DRAW))
        self.assertEqual(game.allowed_actions(2).default, Action(ActionType.NOTHING))
        self.assertEqual(game.allowed_actions(3).default, Action(ActionType.NOTHING))

    def test_wrong_turn_nothing(self):
        game = Game(test_deck)
        self.assertSetEqual(
            game.allowed_actions(1).actions, {Action(ActionType.NOTHING)}
        )
        self.assertSetEqual(
            game.allowed_actions(2).actions, {Action(ActionType.NOTHING)}
        )
        self.assertSetEqual(
            game.allowed_actions(3).actions, {Action(ActionType.NOTHING)}
        )

    def test_turn_discard_actions(self):
        game = Game(test_deck)
        self.assertSetEqual(
            game.allowed_actions(0).actions,
            {
                Action(ActionType.DISCARD, 1),
                Action(ActionType.DISCARD, 2),
                Action(ActionType.DISCARD, 3),
                Action(ActionType.DISCARD, 4),
                Action(ActionType.DISCARD, 5),
                Action(ActionType.DISCARD, 6),
                Action(ActionType.DISCARD, 7),
                Action(ActionType.DISCARD, 8),
                Action(ActionType.DISCARD, 9),
                Action(ActionType.DISCARD, 17),
                Action(ActionType.DISCARD, 21),
            },
        )

    def test_discard_self_cannot_chi(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 1))
        self.assertSetEqual(
            game.allowed_actions(0).actions, {Action(ActionType.NOTHING)}
        )

    def test_discard_self_cannot_pon(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 21))
        self.assertSetEqual(
            game.allowed_actions(0).actions, {Action(ActionType.NOTHING)}
        )

    def test_can_draw(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 17))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {Action(ActionType.DRAW)},
        )

    def test_can_chi_abc(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 5))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(ActionType.DRAW),
                Action(ActionType.CHI_A),
                Action(ActionType.CHI_B),
                Action(ActionType.CHI_C),
            },
        )

    def test_can_pon_kan(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 9))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(ActionType.DRAW),
                Action(ActionType.CHI_C),
                Action(ActionType.PON),
                Action(ActionType.OPEN_KAN),
            },
        )

    def test_discard_actions_after_chi(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 9))
        game.do_action(1, Action(ActionType.CHI_C))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(ActionType.DISCARD, 1),
                Action(ActionType.DISCARD, 2),
                Action(ActionType.DISCARD, 3),
                Action(ActionType.DISCARD, 4),
                Action(ActionType.DISCARD, 5),
                Action(ActionType.DISCARD, 6),
                Action(ActionType.DISCARD, 9),
                Action(ActionType.DISCARD, 17),
                Action(ActionType.DISCARD, 21),
            },
        )

    def test_cannot_kan_after_call(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 9))
        game.do_action(1, Action(ActionType.PON))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(ActionType.DISCARD, 1),
                Action(ActionType.DISCARD, 2),
                Action(ActionType.DISCARD, 3),
                Action(ActionType.DISCARD, 4),
                Action(ActionType.DISCARD, 5),
                Action(ActionType.DISCARD, 6),
                Action(ActionType.DISCARD, 7),
                Action(ActionType.DISCARD, 8),
                Action(ActionType.DISCARD, 9),
                Action(ActionType.DISCARD, 17),
                Action(ActionType.DISCARD, 21),
            },
        )

    def test_can_ron(self):
        game = Game(test_deck2)
        game.do_action(0, Action(ActionType.DISCARD, 13))
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {Action(ActionType.NOTHING), Action(ActionType.RON)},
        )

    def test_can_tsumo(self):
        game = Game(test_deck2)
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.DISCARD, 2))
        game.do_action(2, Action(ActionType.DRAW))
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {
                Action(ActionType.DISCARD, 11),
                Action(ActionType.DISCARD, 12),
                Action(ActionType.DISCARD, 14),
                Action(ActionType.DISCARD, 15),
                Action(ActionType.DISCARD, 16),
                Action(ActionType.DISCARD, 31),
                Action(ActionType.DISCARD, 32),
                Action(ActionType.TSUMO),
            },
        )

    def test_cannot_ron_own_discard(self):
        game = Game(test_deck2)
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.DISCARD, 2))
        game.do_action(2, Action(ActionType.DRAW))
        game.do_action(2, Action(ActionType.DISCARD, 11))
        self.assertSetEqual(
            game.allowed_actions(2).actions, {Action(ActionType.NOTHING)}
        )

    def test_can_chankan(self):
        game = Game(test_deck2)
        game.do_action(0, Action(ActionType.DISCARD, 13))
        game.do_action(1, Action(ActionType.PON))
        game.do_action(1, Action(ActionType.DISCARD, 7))
        game.do_action(0, Action(ActionType.OPEN_KAN))
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.ADD_KAN, 13))
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {Action(ActionType.NOTHING), Action(ActionType.RON)},
        )
