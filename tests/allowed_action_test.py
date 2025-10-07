import unittest

from src.mahjong.action import (
    ActionType,
    AddKanAction,
    ClosedKanAction,
    HandTileAction,
    OpenCallAction,
    OpenKanAction,
    SimpleAction,
)
from src.mahjong.call import CallType, OpenCall
from src.mahjong.game_options import GameOptions
from src.mahjong.round import Round
from tests.decks import test_deck1, test_deck2, test_deck3


class AllowedActionTest(unittest.TestCase):
    def test_play_default_actions(self) -> None:
        round = Round(tiles=test_deck1)
        self.assertEqual(
            round.allowed_actions[0].default.action_type,
            ActionType.DISCARD,
        )
        self.assertEqual(
            round.allowed_actions[1].default, SimpleAction(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[2].default, SimpleAction(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[3].default, SimpleAction(action_type=ActionType.PASS)
        )

    def test_auto_actions(self) -> None:
        round = Round(tiles=test_deck1)
        self.assertEqual(round.allowed_actions[0].auto, None)
        self.assertEqual(
            round.allowed_actions[1].auto, SimpleAction(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[2].auto, SimpleAction(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[3].auto, SimpleAction(action_type=ActionType.PASS)
        )

    def test_discarded_default_actions(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        self.assertEqual(
            round.allowed_actions[0].default, SimpleAction(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[1].default, SimpleAction(action_type=ActionType.DRAW)
        )
        self.assertEqual(
            round.allowed_actions[2].default, SimpleAction(action_type=ActionType.PASS)
        )
        self.assertEqual(
            round.allowed_actions[3].default, SimpleAction(action_type=ActionType.PASS)
        )

    def test_wrong_turn_nothing(self) -> None:
        round = Round(tiles=test_deck1)
        self.assertSequenceEqual(
            round.allowed_actions[1].actions,
            [SimpleAction(action_type=ActionType.PASS)],
        )
        self.assertSequenceEqual(
            round.allowed_actions[2].actions,
            [SimpleAction(action_type=ActionType.PASS)],
        )
        self.assertSequenceEqual(
            round.allowed_actions[3].actions,
            [SimpleAction(action_type=ActionType.PASS)],
        )

    def test_turn_discard_actions(self) -> None:
        round = Round(tiles=test_deck1)
        self.assertSequenceEqual(
            round.allowed_actions[0].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=212),
                HandTileAction(action_type=ActionType.DISCARD, tile=10),
                HandTileAction(action_type=ActionType.DISCARD, tile=12),
                HandTileAction(action_type=ActionType.DISCARD, tile=20),
                HandTileAction(action_type=ActionType.DISCARD, tile=30),
                HandTileAction(action_type=ActionType.DISCARD, tile=40),
                HandTileAction(action_type=ActionType.DISCARD, tile=50),
                HandTileAction(action_type=ActionType.DISCARD, tile=60),
                HandTileAction(action_type=ActionType.DISCARD, tile=70),
                HandTileAction(action_type=ActionType.DISCARD, tile=80),
                HandTileAction(action_type=ActionType.DISCARD, tile=90),
                HandTileAction(action_type=ActionType.DISCARD, tile=170),
                HandTileAction(action_type=ActionType.DISCARD, tile=210),
                HandTileAction(action_type=ActionType.DISCARD, tile=211),
            ],
        )

    def test_discard_self_cannot_chi(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.assertSequenceEqual(
            round.allowed_actions[0].actions,
            [SimpleAction(action_type=ActionType.PASS)],
        )

    def test_discard_self_cannot_pon(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=210))
        self.assertSequenceEqual(
            round.allowed_actions[0].actions,
            [SimpleAction(action_type=ActionType.PASS)],
        )

    def test_can_draw(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=170))
        self.assertSequenceEqual(
            round.allowed_actions[1].actions,
            [SimpleAction(action_type=ActionType.DRAW)],
        )

    def test_can_chi_abc(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        print(round._hands[1].tile_values)
        self.assertSequenceEqual(
            round.allowed_actions[1].actions,
            [
                SimpleAction(action_type=ActionType.DRAW),
                OpenCallAction(action_type=ActionType.CHII, other_tiles=(31, 41)),
                OpenCallAction(action_type=ActionType.CHII, other_tiles=(41, 61)),
                OpenCallAction(action_type=ActionType.CHII, other_tiles=(61, 71)),
            ],
        )

    def test_can_pon_open_kan(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        self.assertSequenceEqual(
            round.allowed_actions[1].actions,
            [
                SimpleAction(action_type=ActionType.DRAW),
                OpenCallAction(action_type=ActionType.CHII, other_tiles=(71, 81)),
                OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92)),
                OpenKanAction(other_tiles=(91, 92, 93)),
            ],
        )

    def test_can_add_kan(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))
        )
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.assertSequenceEqual(
            round.allowed_actions[1].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=13),
                HandTileAction(action_type=ActionType.DISCARD, tile=11),
                HandTileAction(action_type=ActionType.DISCARD, tile=21),
                HandTileAction(action_type=ActionType.DISCARD, tile=31),
                HandTileAction(action_type=ActionType.DISCARD, tile=41),
                HandTileAction(action_type=ActionType.DISCARD, tile=51),
                HandTileAction(action_type=ActionType.DISCARD, tile=61),
                HandTileAction(action_type=ActionType.DISCARD, tile=71),
                HandTileAction(action_type=ActionType.DISCARD, tile=81),
                HandTileAction(action_type=ActionType.DISCARD, tile=93),
                HandTileAction(action_type=ActionType.DISCARD, tile=171),
                AddKanAction(
                    tile=93,
                    pon_call=OpenCall(
                        call_type=CallType.PON,
                        called_player_index=0,
                        called_tile=90,
                        other_tiles=(91, 92),
                    ),
                ),
            ],
        )

    def test_can_closed_kan(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        self.assertSequenceEqual(
            round.allowed_actions[2].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=22),
                HandTileAction(action_type=ActionType.DISCARD, tile=110),
                HandTileAction(action_type=ActionType.DISCARD, tile=111),
                HandTileAction(action_type=ActionType.DISCARD, tile=112),
                HandTileAction(action_type=ActionType.DISCARD, tile=113),
                HandTileAction(action_type=ActionType.DISCARD, tile=130),
                HandTileAction(action_type=ActionType.DISCARD, tile=131),
                HandTileAction(action_type=ActionType.DISCARD, tile=132),
                HandTileAction(action_type=ActionType.DISCARD, tile=133),
                HandTileAction(action_type=ActionType.DISCARD, tile=150),
                HandTileAction(action_type=ActionType.DISCARD, tile=151),
                HandTileAction(action_type=ActionType.DISCARD, tile=152),
                HandTileAction(action_type=ActionType.DISCARD, tile=153),
                HandTileAction(action_type=ActionType.DISCARD, tile=172),
                ClosedKanAction(tiles=(110, 111, 112, 113)),
                ClosedKanAction(tiles=(130, 131, 132, 133)),
                ClosedKanAction(tiles=(150, 151, 152, 153)),
            ],
        )

    def test_discard_actions_after_chi(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.CHII, other_tiles=(71, 81))
        )
        self.assertSequenceEqual(
            round.allowed_actions[1].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=213),
                HandTileAction(action_type=ActionType.DISCARD, tile=11),
                HandTileAction(action_type=ActionType.DISCARD, tile=21),
                HandTileAction(action_type=ActionType.DISCARD, tile=31),
                HandTileAction(action_type=ActionType.DISCARD, tile=41),
                HandTileAction(action_type=ActionType.DISCARD, tile=51),
                HandTileAction(action_type=ActionType.DISCARD, tile=61),
                HandTileAction(action_type=ActionType.DISCARD, tile=91),
                HandTileAction(action_type=ActionType.DISCARD, tile=92),
                HandTileAction(action_type=ActionType.DISCARD, tile=93),
                HandTileAction(action_type=ActionType.DISCARD, tile=171),
            ],
        )

    def test_cannot_kan_after_call(self) -> None:
        round = Round(tiles=test_deck1)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        self.assertSequenceEqual(
            round.allowed_actions[1].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=213),
                HandTileAction(action_type=ActionType.DISCARD, tile=11),
                HandTileAction(action_type=ActionType.DISCARD, tile=21),
                HandTileAction(action_type=ActionType.DISCARD, tile=31),
                HandTileAction(action_type=ActionType.DISCARD, tile=41),
                HandTileAction(action_type=ActionType.DISCARD, tile=51),
                HandTileAction(action_type=ActionType.DISCARD, tile=61),
                HandTileAction(action_type=ActionType.DISCARD, tile=71),
                HandTileAction(action_type=ActionType.DISCARD, tile=81),
                HandTileAction(action_type=ActionType.DISCARD, tile=93),
                HandTileAction(action_type=ActionType.DISCARD, tile=171),
            ],
        )

    def test_can_ron(self) -> None:
        round = Round(tiles=test_deck2)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        self.assertSequenceEqual(
            round.allowed_actions[2].actions,
            [
                SimpleAction(action_type=ActionType.PASS),
                SimpleAction(action_type=ActionType.RON),
            ],
        )

    def test_can_tsumo(self) -> None:
        round = Round(tiles=test_deck2)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        self.assertSequenceEqual(
            round.allowed_actions[2].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=160),
                HandTileAction(action_type=ActionType.DISCARD, tile=110),
                HandTileAction(action_type=ActionType.DISCARD, tile=111),
                HandTileAction(action_type=ActionType.DISCARD, tile=112),
                HandTileAction(action_type=ActionType.DISCARD, tile=120),
                HandTileAction(action_type=ActionType.DISCARD, tile=121),
                HandTileAction(action_type=ActionType.DISCARD, tile=122),
                HandTileAction(action_type=ActionType.DISCARD, tile=140),
                HandTileAction(action_type=ActionType.DISCARD, tile=150),
                HandTileAction(action_type=ActionType.DISCARD, tile=310),
                HandTileAction(action_type=ActionType.DISCARD, tile=311),
                HandTileAction(action_type=ActionType.DISCARD, tile=320),
                HandTileAction(action_type=ActionType.DISCARD, tile=321),
                HandTileAction(action_type=ActionType.DISCARD, tile=322),
                SimpleAction(action_type=ActionType.TSUMO),
            ],
        )

    def test_cannot_ron_own_discard(self) -> None:
        round = Round(tiles=test_deck2)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=110))
        self.assertSequenceEqual(
            round.allowed_actions[2].actions,
            [SimpleAction(action_type=ActionType.PASS)],
        )

    def test_can_chankan(self) -> None:
        round = Round(tiles=test_deck2)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(131, 132))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=73))
        round.do_action(0, OpenKanAction(other_tiles=(70, 71, 72)))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(
            1,
            AddKanAction(
                tile=133,
                pon_call=OpenCall(
                    call_type=CallType.PON,
                    called_player_index=0,
                    called_tile=130,
                    other_tiles=(131, 132),
                ),
            ),
        )
        self.assertSequenceEqual(
            round.allowed_actions[2].actions,
            [
                SimpleAction(action_type=ActionType.PASS),
                SimpleAction(action_type=ActionType.RON),
            ],
        )

    def test_start_flowers(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        self.assertSequenceEqual(
            round.allowed_actions[0].actions,
            [
                SimpleAction(action_type=ActionType.CONTINUE),
                HandTileAction(action_type=ActionType.FLOWER, tile=410),
                HandTileAction(action_type=ActionType.FLOWER, tile=430),
            ],
        )

    def test_start_wrong_player_flowers(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        self.assertSequenceEqual(
            round.allowed_actions[1].actions,
            [SimpleAction(action_type=ActionType.PASS)],
        )

    def test_manual_can_flower(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=420))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        self.assertSequenceEqual(
            round.allowed_actions[2].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=450),
                HandTileAction(action_type=ActionType.DISCARD, tile=30),
                HandTileAction(action_type=ActionType.DISCARD, tile=31),
                HandTileAction(action_type=ActionType.DISCARD, tile=32),
                HandTileAction(action_type=ActionType.DISCARD, tile=33),
                HandTileAction(action_type=ActionType.DISCARD, tile=70),
                HandTileAction(action_type=ActionType.DISCARD, tile=71),
                HandTileAction(action_type=ActionType.DISCARD, tile=72),
                HandTileAction(action_type=ActionType.DISCARD, tile=73),
                HandTileAction(action_type=ActionType.DISCARD, tile=90),
                HandTileAction(action_type=ActionType.DISCARD, tile=130),
                HandTileAction(action_type=ActionType.DISCARD, tile=131),
                HandTileAction(action_type=ActionType.DISCARD, tile=132),
                HandTileAction(action_type=ActionType.DISCARD, tile=133),
                ClosedKanAction(tiles=(30, 31, 32, 33)),
                ClosedKanAction(tiles=(70, 71, 72, 73)),
                ClosedKanAction(tiles=(130, 131, 132, 133)),
                HandTileAction(action_type=ActionType.FLOWER, tile=450),
            ],
        )

    def test_auto_must_flower(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=True))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        self.assertSequenceEqual(
            round.allowed_actions[2].actions,
            [
                HandTileAction(action_type=ActionType.FLOWER, tile=450),
            ],
        )
