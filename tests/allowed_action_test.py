import unittest

from src.mahjong.action import Action, ActionType
from src.mahjong.game import Game, GameOptions

from tests.decks import test_deck1, test_deck2, test_deck3


class AllowedActionTest(unittest.TestCase):
    def test_play_default_actions(self):
        game = Game(test_deck1)
        self.assertEqual(
            game.allowed_actions(0).default.action_type,
            ActionType.DISCARD,
        )
        self.assertEqual(
            game.allowed_actions(1).default, Action(action_type=ActionType.NOTHING)
        )
        self.assertEqual(
            game.allowed_actions(2).default, Action(action_type=ActionType.NOTHING)
        )
        self.assertEqual(
            game.allowed_actions(3).default, Action(action_type=ActionType.NOTHING)
        )

    def test_discarded_default_actions(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertEqual(
            game.allowed_actions(0).default, Action(action_type=ActionType.NOTHING)
        )
        self.assertEqual(
            game.allowed_actions(1).default, Action(action_type=ActionType.DRAW)
        )
        self.assertEqual(
            game.allowed_actions(2).default, Action(action_type=ActionType.NOTHING)
        )
        self.assertEqual(
            game.allowed_actions(3).default, Action(action_type=ActionType.NOTHING)
        )

    def test_wrong_turn_nothing(self):
        game = Game(test_deck1)
        self.assertSetEqual(
            game.allowed_actions(1).actions, {Action(action_type=ActionType.NOTHING)}
        )
        self.assertSetEqual(
            game.allowed_actions(2).actions, {Action(action_type=ActionType.NOTHING)}
        )
        self.assertSetEqual(
            game.allowed_actions(3).actions, {Action(action_type=ActionType.NOTHING)}
        )

    def test_turn_discard_actions(self):
        game = Game(test_deck1)
        self.assertSetEqual(
            game.allowed_actions(0).actions,
            {
                Action(action_type=ActionType.DISCARD, tile=1),
                Action(action_type=ActionType.DISCARD, tile=2),
                Action(action_type=ActionType.DISCARD, tile=3),
                Action(action_type=ActionType.DISCARD, tile=4),
                Action(action_type=ActionType.DISCARD, tile=5),
                Action(action_type=ActionType.DISCARD, tile=6),
                Action(action_type=ActionType.DISCARD, tile=7),
                Action(action_type=ActionType.DISCARD, tile=8),
                Action(action_type=ActionType.DISCARD, tile=9),
                Action(action_type=ActionType.DISCARD, tile=17),
                Action(action_type=ActionType.DISCARD, tile=21),
            },
        )

    def test_discard_self_cannot_chi(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        self.assertSetEqual(
            game.allowed_actions(0).actions, {Action(action_type=ActionType.NOTHING)}
        )

    def test_discard_self_cannot_pon(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=21))
        self.assertSetEqual(
            game.allowed_actions(0).actions, {Action(action_type=ActionType.NOTHING)}
        )

    def test_can_draw(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=17))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {Action(action_type=ActionType.DRAW)},
        )

    def test_can_chi_abc(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=5))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(action_type=ActionType.DRAW),
                Action(action_type=ActionType.CHI_A),
                Action(action_type=ActionType.CHI_B),
                Action(action_type=ActionType.CHI_C),
            },
        )

    def test_can_pon_kan(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(action_type=ActionType.DRAW),
                Action(action_type=ActionType.CHI_C),
                Action(action_type=ActionType.PON),
                Action(action_type=ActionType.OPEN_KAN),
            },
        )

    def test_discard_actions_after_chi(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        game.do_action(1, Action(action_type=ActionType.CHI_C))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(action_type=ActionType.DISCARD, tile=1),
                Action(action_type=ActionType.DISCARD, tile=2),
                Action(action_type=ActionType.DISCARD, tile=3),
                Action(action_type=ActionType.DISCARD, tile=4),
                Action(action_type=ActionType.DISCARD, tile=5),
                Action(action_type=ActionType.DISCARD, tile=6),
                Action(action_type=ActionType.DISCARD, tile=9),
                Action(action_type=ActionType.DISCARD, tile=17),
                Action(action_type=ActionType.DISCARD, tile=21),
            },
        )

    def test_cannot_kan_after_call(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        game.do_action(1, Action(action_type=ActionType.PON))
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(action_type=ActionType.DISCARD, tile=1),
                Action(action_type=ActionType.DISCARD, tile=2),
                Action(action_type=ActionType.DISCARD, tile=3),
                Action(action_type=ActionType.DISCARD, tile=4),
                Action(action_type=ActionType.DISCARD, tile=5),
                Action(action_type=ActionType.DISCARD, tile=6),
                Action(action_type=ActionType.DISCARD, tile=7),
                Action(action_type=ActionType.DISCARD, tile=8),
                Action(action_type=ActionType.DISCARD, tile=9),
                Action(action_type=ActionType.DISCARD, tile=17),
                Action(action_type=ActionType.DISCARD, tile=21),
            },
        )

    def test_can_ron(self):
        game = Game(test_deck2)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {
                Action(action_type=ActionType.NOTHING),
                Action(action_type=ActionType.RON),
            },
        )

    def test_can_tsumo(self):
        game = Game(test_deck2)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        game.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {
                Action(action_type=ActionType.DISCARD, tile=11),
                Action(action_type=ActionType.DISCARD, tile=12),
                Action(action_type=ActionType.DISCARD, tile=14),
                Action(action_type=ActionType.DISCARD, tile=15),
                Action(action_type=ActionType.DISCARD, tile=16),
                Action(action_type=ActionType.DISCARD, tile=31),
                Action(action_type=ActionType.DISCARD, tile=32),
                Action(action_type=ActionType.TSUMO),
            },
        )

    def test_cannot_ron_own_discard(self):
        game = Game(test_deck2)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        game.do_action(2, Action(action_type=ActionType.DRAW))
        game.do_action(2, Action(action_type=ActionType.DISCARD, tile=11))
        self.assertSetEqual(
            game.allowed_actions(2).actions, {Action(action_type=ActionType.NOTHING)}
        )

    def test_can_chankan(self):
        game = Game(test_deck2)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        game.do_action(1, Action(action_type=ActionType.PON))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=7))
        game.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=13))
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {
                Action(action_type=ActionType.NOTHING),
                Action(action_type=ActionType.RON),
            },
        )

    def test_start_flowers(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        self.assertSetEqual(
            game.allowed_actions(0).actions,
            {
                Action(action_type=ActionType.NOTHING),
                Action(action_type=ActionType.FLOWER, tile=41),
                Action(action_type=ActionType.FLOWER, tile=43),
            },
        )

    def test_start_wrong_player_flowers(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        self.assertSetEqual(
            game.allowed_actions(1).actions, {Action(action_type=ActionType.NOTHING)}
        )

    def test_manual_can_flower(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(2, Action(action_type=ActionType.NOTHING))
        game.do_action(3, Action(action_type=ActionType.NOTHING))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(2, Action(action_type=ActionType.NOTHING))
        game.do_action(3, Action(action_type=ActionType.NOTHING))
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        game.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {
                Action(action_type=ActionType.DISCARD, tile=3),
                Action(action_type=ActionType.DISCARD, tile=7),
                Action(action_type=ActionType.DISCARD, tile=9),
                Action(action_type=ActionType.DISCARD, tile=13),
                Action(action_type=ActionType.DISCARD, tile=45),
                Action(action_type=ActionType.CLOSED_KAN, tile=3),
                Action(action_type=ActionType.CLOSED_KAN, tile=7),
                Action(action_type=ActionType.CLOSED_KAN, tile=13),
                Action(action_type=ActionType.FLOWER, tile=45),
            },
        )

    def test_auto_must_flower(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=True))
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        game.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {
                Action(action_type=ActionType.FLOWER, tile=45),
            },
        )
