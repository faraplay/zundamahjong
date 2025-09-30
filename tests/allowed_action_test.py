import unittest

from src.mahjong.action import Action, ActionType
from src.mahjong.game_options import GameOptions
from src.mahjong.round import Round
from tests.decks import test_deck1, test_deck2, test_deck3


class AllowedActionTest(unittest.TestCase):
    def test_play_default_actions(self):
        round = Round(tiles=test_deck1)
        self.assertEqual(
            round.allowed_actions[0].default.action_type,
            ActionType.DISCARD,
        )
        self.assertEqual(
            round.allowed_actions[1].default, Action(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[2].default, Action(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[3].default, Action(action_type=ActionType.PASS)
        )

    def test_auto_actions(self):
        round = Round(tiles=test_deck1)
        self.assertEqual(round.allowed_actions[0].auto, None)
        self.assertEqual(
            round.allowed_actions[1].auto, Action(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[2].auto, Action(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[3].auto, Action(action_type=ActionType.PASS)
        )

    def test_discarded_default_actions(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=90))
        self.assertEqual(
            round.allowed_actions[0].default, Action(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[1].default, Action(action_type=ActionType.DRAW)
        )
        self.assertEqual(
            round.allowed_actions[2].default, Action(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[3].default, Action(action_type=ActionType.PASS)
        )

    def test_wrong_turn_nothing(self):
        round = Round(tiles=test_deck1)
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {Action(action_type=ActionType.PASS)},
        )
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {Action(action_type=ActionType.PASS)},
        )
        self.assertSetEqual(
            round.allowed_actions[3].actions,
            {Action(action_type=ActionType.PASS)},
        )

    def test_turn_discard_actions(self):
        round = Round(tiles=test_deck1)
        self.assertSetEqual(
            round.allowed_actions[0].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=10),
                Action(action_type=ActionType.DISCARD, tile=20),
                Action(action_type=ActionType.DISCARD, tile=30),
                Action(action_type=ActionType.DISCARD, tile=40),
                Action(action_type=ActionType.DISCARD, tile=50),
                Action(action_type=ActionType.DISCARD, tile=60),
                Action(action_type=ActionType.DISCARD, tile=70),
                Action(action_type=ActionType.DISCARD, tile=80),
                Action(action_type=ActionType.DISCARD, tile=90),
                Action(action_type=ActionType.DISCARD, tile=210),
                Action(action_type=ActionType.DISCARD, tile=211),
                Action(action_type=ActionType.DISCARD, tile=212),
                Action(action_type=ActionType.DISCARD, tile=170),
                Action(action_type=ActionType.DISCARD, tile=12),
            },
        )

    def test_discard_self_cannot_chi(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        self.assertSetEqual(
            round.allowed_actions[0].actions,
            {Action(action_type=ActionType.PASS)},
        )

    def test_discard_self_cannot_pon(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=210))
        self.assertSetEqual(
            round.allowed_actions[0].actions,
            {Action(action_type=ActionType.PASS)},
        )

    def test_can_draw(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=170))
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {Action(action_type=ActionType.DRAW)},
        )

    def test_can_chi_abc(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=50))
        print(round._hands[1].tile_values)
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {
                Action(action_type=ActionType.DRAW),
                Action(action_type=ActionType.CHI_A),
                Action(action_type=ActionType.CHI_B),
                Action(action_type=ActionType.CHI_C),
            },
        )

    def test_can_pon_kan(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=90))
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {
                Action(action_type=ActionType.DRAW),
                Action(action_type=ActionType.CHI_C),
                Action(action_type=ActionType.PON),
                Action(action_type=ActionType.OPEN_KAN),
            },
        )

    def test_discard_actions_after_chi(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=90))
        round.do_action(1, Action(action_type=ActionType.CHI_C))
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=11),
                Action(action_type=ActionType.DISCARD, tile=21),
                Action(action_type=ActionType.DISCARD, tile=31),
                Action(action_type=ActionType.DISCARD, tile=41),
                Action(action_type=ActionType.DISCARD, tile=51),
                Action(action_type=ActionType.DISCARD, tile=61),
                Action(action_type=ActionType.DISCARD, tile=91),
                Action(action_type=ActionType.DISCARD, tile=92),
                Action(action_type=ActionType.DISCARD, tile=93),
                Action(action_type=ActionType.DISCARD, tile=213),
                Action(action_type=ActionType.DISCARD, tile=171),
            },
        )

    def test_cannot_kan_after_call(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=90))
        round.do_action(1, Action(action_type=ActionType.PON))
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=11),
                Action(action_type=ActionType.DISCARD, tile=21),
                Action(action_type=ActionType.DISCARD, tile=31),
                Action(action_type=ActionType.DISCARD, tile=41),
                Action(action_type=ActionType.DISCARD, tile=51),
                Action(action_type=ActionType.DISCARD, tile=61),
                Action(action_type=ActionType.DISCARD, tile=71),
                Action(action_type=ActionType.DISCARD, tile=81),
                Action(action_type=ActionType.DISCARD, tile=93),
                Action(action_type=ActionType.DISCARD, tile=213),
                Action(action_type=ActionType.DISCARD, tile=171),
            },
        )

    def test_can_ron(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.PASS),
                Action(action_type=ActionType.RON),
            },
        )

    def test_can_tsumo(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=110),
                Action(action_type=ActionType.DISCARD, tile=111),
                Action(action_type=ActionType.DISCARD, tile=112),
                Action(action_type=ActionType.DISCARD, tile=120),
                Action(action_type=ActionType.DISCARD, tile=121),
                Action(action_type=ActionType.DISCARD, tile=122),
                Action(action_type=ActionType.DISCARD, tile=310),
                Action(action_type=ActionType.DISCARD, tile=311),
                Action(action_type=ActionType.DISCARD, tile=320),
                Action(action_type=ActionType.DISCARD, tile=321),
                Action(action_type=ActionType.DISCARD, tile=322),
                Action(action_type=ActionType.DISCARD, tile=140),
                Action(action_type=ActionType.DISCARD, tile=150),
                Action(action_type=ActionType.DISCARD, tile=160),
                Action(action_type=ActionType.TSUMO),
            },
        )

    def test_cannot_ron_own_discard(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.DISCARD, tile=110))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {Action(action_type=ActionType.PASS)},
        )

    def test_can_chankan(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=73))
        round.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=133))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.PASS),
                Action(action_type=ActionType.RON),
            },
        )

    def test_start_flowers(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        self.assertSetEqual(
            round.allowed_actions[0].actions,
            {
                Action(action_type=ActionType.CONTINUE),
                Action(action_type=ActionType.FLOWER, tile=410),
                Action(action_type=ActionType.FLOWER, tile=430),
            },
        )

    def test_start_wrong_player_flowers(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {Action(action_type=ActionType.PASS)},
        )

    def test_manual_can_flower(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=420))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=30),
                Action(action_type=ActionType.DISCARD, tile=31),
                Action(action_type=ActionType.DISCARD, tile=32),
                Action(action_type=ActionType.DISCARD, tile=33),
                Action(action_type=ActionType.DISCARD, tile=70),
                Action(action_type=ActionType.DISCARD, tile=71),
                Action(action_type=ActionType.DISCARD, tile=72),
                Action(action_type=ActionType.DISCARD, tile=73),
                Action(action_type=ActionType.DISCARD, tile=130),
                Action(action_type=ActionType.DISCARD, tile=131),
                Action(action_type=ActionType.DISCARD, tile=132),
                Action(action_type=ActionType.DISCARD, tile=133),
                Action(action_type=ActionType.DISCARD, tile=90),
                Action(action_type=ActionType.DISCARD, tile=450),
                Action(action_type=ActionType.CLOSED_KAN, tile=30),
                Action(action_type=ActionType.CLOSED_KAN, tile=70),
                Action(action_type=ActionType.CLOSED_KAN, tile=130),
                Action(action_type=ActionType.FLOWER, tile=450),
            },
        )

    def test_auto_must_flower(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=True))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.FLOWER, tile=450),
            },
        )
