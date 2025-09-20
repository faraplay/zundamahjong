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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=36))
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
                Action(action_type=ActionType.DISCARD, tile=4),
                Action(action_type=ActionType.DISCARD, tile=8),
                Action(action_type=ActionType.DISCARD, tile=12),
                Action(action_type=ActionType.DISCARD, tile=16),
                Action(action_type=ActionType.DISCARD, tile=20),
                Action(action_type=ActionType.DISCARD, tile=24),
                Action(action_type=ActionType.DISCARD, tile=28),
                Action(action_type=ActionType.DISCARD, tile=32),
                Action(action_type=ActionType.DISCARD, tile=36),
                Action(action_type=ActionType.DISCARD, tile=84),
                Action(action_type=ActionType.DISCARD, tile=85),
                Action(action_type=ActionType.DISCARD, tile=86),
                Action(action_type=ActionType.DISCARD, tile=68),
                Action(action_type=ActionType.DISCARD, tile=6),
            },
        )

    def test_discard_self_cannot_chi(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        self.assertSetEqual(
            round.allowed_actions[0].actions,
            {Action(action_type=ActionType.PASS)},
        )

    def test_discard_self_cannot_pon(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=84))
        self.assertSetEqual(
            round.allowed_actions[0].actions,
            {Action(action_type=ActionType.PASS)},
        )

    def test_can_draw(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=68))
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {Action(action_type=ActionType.DRAW)},
        )

    def test_can_chi_abc(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=20))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=36))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=36))
        round.do_action(1, Action(action_type=ActionType.CHI_C))
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=5),
                Action(action_type=ActionType.DISCARD, tile=9),
                Action(action_type=ActionType.DISCARD, tile=13),
                Action(action_type=ActionType.DISCARD, tile=17),
                Action(action_type=ActionType.DISCARD, tile=21),
                Action(action_type=ActionType.DISCARD, tile=25),
                Action(action_type=ActionType.DISCARD, tile=37),
                Action(action_type=ActionType.DISCARD, tile=38),
                Action(action_type=ActionType.DISCARD, tile=39),
                Action(action_type=ActionType.DISCARD, tile=87),
                Action(action_type=ActionType.DISCARD, tile=69),
            },
        )

    def test_cannot_kan_after_call(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=36))
        round.do_action(1, Action(action_type=ActionType.PON))
        self.assertSetEqual(
            round.allowed_actions[1].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=5),
                Action(action_type=ActionType.DISCARD, tile=9),
                Action(action_type=ActionType.DISCARD, tile=13),
                Action(action_type=ActionType.DISCARD, tile=17),
                Action(action_type=ActionType.DISCARD, tile=21),
                Action(action_type=ActionType.DISCARD, tile=25),
                Action(action_type=ActionType.DISCARD, tile=29),
                Action(action_type=ActionType.DISCARD, tile=33),
                Action(action_type=ActionType.DISCARD, tile=39),
                Action(action_type=ActionType.DISCARD, tile=87),
                Action(action_type=ActionType.DISCARD, tile=69),
            },
        )

    def test_can_ron(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.PASS),
                Action(action_type=ActionType.RON),
            },
        )

    def test_can_tsumo(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=8))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=44),
                Action(action_type=ActionType.DISCARD, tile=45),
                Action(action_type=ActionType.DISCARD, tile=46),
                Action(action_type=ActionType.DISCARD, tile=48),
                Action(action_type=ActionType.DISCARD, tile=49),
                Action(action_type=ActionType.DISCARD, tile=50),
                Action(action_type=ActionType.DISCARD, tile=124),
                Action(action_type=ActionType.DISCARD, tile=125),
                Action(action_type=ActionType.DISCARD, tile=128),
                Action(action_type=ActionType.DISCARD, tile=129),
                Action(action_type=ActionType.DISCARD, tile=130),
                Action(action_type=ActionType.DISCARD, tile=56),
                Action(action_type=ActionType.DISCARD, tile=60),
                Action(action_type=ActionType.DISCARD, tile=64),
                Action(action_type=ActionType.TSUMO),
            },
        )

    def test_cannot_ron_own_discard(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=8))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.DISCARD, tile=44))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {Action(action_type=ActionType.PASS)},
        )

    def test_can_chankan(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=31))
        round.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=55))
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
                Action(action_type=ActionType.FLOWER, tile=164),
                Action(action_type=ActionType.FLOWER, tile=172),
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
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=164))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=172))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=168))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=176))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=8))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.DISCARD, tile=12),
                Action(action_type=ActionType.DISCARD, tile=13),
                Action(action_type=ActionType.DISCARD, tile=14),
                Action(action_type=ActionType.DISCARD, tile=15),
                Action(action_type=ActionType.DISCARD, tile=28),
                Action(action_type=ActionType.DISCARD, tile=29),
                Action(action_type=ActionType.DISCARD, tile=30),
                Action(action_type=ActionType.DISCARD, tile=31),
                Action(action_type=ActionType.DISCARD, tile=52),
                Action(action_type=ActionType.DISCARD, tile=53),
                Action(action_type=ActionType.DISCARD, tile=54),
                Action(action_type=ActionType.DISCARD, tile=55),
                Action(action_type=ActionType.DISCARD, tile=36),
                Action(action_type=ActionType.DISCARD, tile=180),
                Action(action_type=ActionType.CLOSED_KAN, tile=12),
                Action(action_type=ActionType.CLOSED_KAN, tile=28),
                Action(action_type=ActionType.CLOSED_KAN, tile=52),
                Action(action_type=ActionType.FLOWER, tile=180),
            },
        )

    def test_auto_must_flower(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=True))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=8))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        self.assertSetEqual(
            round.allowed_actions[2].actions,
            {
                Action(action_type=ActionType.FLOWER, tile=180),
            },
        )
