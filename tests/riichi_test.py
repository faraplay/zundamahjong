import unittest

from tests.decks import test_deck_riichi
from zundamahjong.mahjong.action import (
    ActionType,
    HandTileAction,
    ClosedKanAction,
    OpenCallAction,
    OpenKanAction,
    SimpleAction,
)
from zundamahjong.mahjong.game_options import GameOptions
from zundamahjong.mahjong.round import Round


def get_round() -> Round:
    return Round(tiles=test_deck_riichi, options=GameOptions(allow_riichi=True))


class RiichiTest(unittest.TestCase):
    def test_riichi_actions(self) -> None:
        round = get_round()
        self.assertSequenceEqual(
            round.allowed_actions[0].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=230),
                HandTileAction(action_type=ActionType.DISCARD, tile=10),
                HandTileAction(action_type=ActionType.DISCARD, tile=11),
                HandTileAction(action_type=ActionType.DISCARD, tile=12),
                HandTileAction(action_type=ActionType.DISCARD, tile=130),
                HandTileAction(action_type=ActionType.DISCARD, tile=140),
                HandTileAction(action_type=ActionType.DISCARD, tile=150),
                HandTileAction(action_type=ActionType.DISCARD, tile=151),
                HandTileAction(action_type=ActionType.DISCARD, tile=152),
                HandTileAction(action_type=ActionType.DISCARD, tile=153),
                HandTileAction(action_type=ActionType.DISCARD, tile=160),
                HandTileAction(action_type=ActionType.DISCARD, tile=220),
                HandTileAction(action_type=ActionType.DISCARD, tile=221),
                HandTileAction(action_type=ActionType.DISCARD, tile=222),
                HandTileAction(action_type=ActionType.RIICHI, tile=130),
                HandTileAction(action_type=ActionType.RIICHI, tile=160),
                HandTileAction(action_type=ActionType.RIICHI, tile=230),
                ClosedKanAction(tiles=(150, 151, 152, 153)),
            ],
        )

    def test_no_riichi_if_call(self) -> None:
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=160))
        round.do_action(
            3, OpenCallAction(action_type=ActionType.PON, other_tiles=(161, 162))
        )
        self.assertNotIn(
            HandTileAction(action_type=ActionType.RIICHI, tile=51),
            round.allowed_actions[3].actions,
        )
        self.assertNotIn(
            HandTileAction(action_type=ActionType.RIICHI, tile=61),
            round.allowed_actions[3].actions,
        )

    def test_can_riichi_with_closed_kan(self) -> None:
        round = get_round()
        round.do_action(0, ClosedKanAction(tiles=(150, 151, 152, 153)))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.assertSequenceEqual(
            round.allowed_actions[0].actions,
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=120),
                HandTileAction(action_type=ActionType.DISCARD, tile=10),
                HandTileAction(action_type=ActionType.DISCARD, tile=11),
                HandTileAction(action_type=ActionType.DISCARD, tile=12),
                HandTileAction(action_type=ActionType.DISCARD, tile=130),
                HandTileAction(action_type=ActionType.DISCARD, tile=140),
                HandTileAction(action_type=ActionType.DISCARD, tile=160),
                HandTileAction(action_type=ActionType.DISCARD, tile=220),
                HandTileAction(action_type=ActionType.DISCARD, tile=221),
                HandTileAction(action_type=ActionType.DISCARD, tile=222),
                HandTileAction(action_type=ActionType.DISCARD, tile=230),
                HandTileAction(action_type=ActionType.RIICHI, tile=160),
                HandTileAction(action_type=ActionType.RIICHI, tile=230),
            ],
        )

    def test_riichi_discard_drawn_tile(self) -> None:
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=160))
        round.do_action(
            3, OpenCallAction(action_type=ActionType.PON, other_tiles=(161, 162))
        )
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=51))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        self.assertSequenceEqual(
            [
                action
                for action in round.allowed_actions[0].actions
                if action.action_type == ActionType.DISCARD
            ],
            [
                HandTileAction(action_type=ActionType.DISCARD, tile=350),
            ],
        )

    def test_no_calls_during_riichi(self) -> None:
        # control test without riichi
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=350))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=13))
        self.assertIn(
            OpenCallAction(action_type=ActionType.PON, other_tiles=(10, 11)),
            round.allowed_actions[0].actions,
        )
        self.assertIn(
            OpenKanAction(other_tiles=(10, 11, 12)),
            round.allowed_actions[0].actions,
        )

        # test with riichi
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=130))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=350))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=13))
        self.assertNotIn(
            OpenCallAction(action_type=ActionType.PON, other_tiles=(10, 11)),
            round.allowed_actions[0].actions,
        )
        self.assertNotIn(
            OpenKanAction(other_tiles=(10, 11, 12)),
            round.allowed_actions[0].actions,
        )

    def test_no_closed_kan_break_tenpai_during_riichi(self) -> None:
        # control test without riichi
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=160))
        round.do_action(
            3, OpenCallAction(action_type=ActionType.PON, other_tiles=(161, 162))
        )
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=51))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        self.assertIn(
            ClosedKanAction(tiles=(150, 151, 152, 153)),
            round.allowed_actions[0].actions,
        )

        # test with riichi
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=160))
        round.do_action(
            3, OpenCallAction(action_type=ActionType.PON, other_tiles=(161, 162))
        )
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=51))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        self.assertNotIn(
            ClosedKanAction(tiles=(150, 151, 152, 153)),
            round.allowed_actions[0].actions,
        )

    def test_closed_kan_during_riichi(self) -> None:
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=230))
        round.do_action(
            2, OpenCallAction(action_type=ActionType.PON, other_tiles=(231, 232))
        )
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(3, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=51))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        self.assertIn(
            ClosedKanAction(tiles=(10, 11, 12, 13)),
            round.allowed_actions[0].actions,
        )

    def test_no_closed_kan_change_wait_during_riichi(self) -> None:
        # control test without riichi
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(131, 132))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=333))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(3, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=51))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        self.assertIn(
            ClosedKanAction(tiles=(220, 221, 222, 223)),
            round.allowed_actions[0].actions,
        )

        # test with riichi
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=130))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(131, 132))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=333))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(3, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=51))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        self.assertNotIn(
            ClosedKanAction(tiles=(220, 221, 222, 223)),
            round.allowed_actions[0].actions,
        )

    def test_riichi_ippatsu(self) -> None:
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=160))
        round.do_action(
            3, OpenCallAction(action_type=ActionType.PON, other_tiles=(161, 162))
        )
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=51))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=350))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=13))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=231))
        round.do_action(0, SimpleAction(action_type=ActionType.RON))
        assert round.win_info is not None
        self.assertTrue(round.win_info.is_riichi)
        self.assertFalse(round.win_info.is_double_riichi)
        self.assertTrue(round.win_info.is_ippatsu)

    def test_double_riichi(self) -> None:
        round = get_round()
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=160))
        round.do_action(
            3, OpenCallAction(action_type=ActionType.PON, other_tiles=(161, 162))
        )
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=51))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=350))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=13))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=231))
        round.do_action(0, SimpleAction(action_type=ActionType.RON))
        assert round.win_info is not None
        self.assertTrue(round.win_info.is_riichi)
        self.assertTrue(round.win_info.is_double_riichi)
        self.assertFalse(round.win_info.is_ippatsu)
