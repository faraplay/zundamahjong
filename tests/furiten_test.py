# pyright: reportPrivateUsage=false

import unittest

from tests.decks import test_deck_furiten
from zundamahjong.mahjong.action import (
    ActionType,
    AddKanAction,
    ClosedKanAction,
    HandTileAction,
    OpenCallAction,
    SimpleAction,
)
from zundamahjong.mahjong.call import (
    CallType,
    OpenCall,
)
from zundamahjong.mahjong.game_options import GameOptions
from zundamahjong.mahjong.round import Round


class TemporaryFuritenTest(unittest.TestCase):
    def test_furiten_deck_hands(self) -> None:
        round = Round(tiles=test_deck_furiten)
        self.assertCountEqual(
            round.get_hand(0),
            [40, 41, 42, 50, 60, 70, 71, 72, 73, 110, 111, 112, 190, 191],
        )
        self.assertCountEqual(
            round.get_hand(1),
            [43, 80, 90, 310, 212, 213, 220, 221, 232, 233, 240, 241, 252],
        )
        self.assertCountEqual(
            round.get_hand(2),
            [51, 61, 130, 131, 132, 140, 141, 142, 150, 151, 152, 192, 193],
        )
        self.assertCountEqual(
            round.get_hand(3),
            [311, 312, 210, 211, 222, 223, 230, 231, 242, 243, 250, 251, 253],
        )

    def test_temp_no_furiten_on_discard(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertFalse(round._hands[2].is_temporary_furiten)

    def test_temp_furiten_after_discard(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertTrue(round._hands[2].is_temporary_furiten)

    def test_temp_furiten_after_second_discard(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertTrue(round._hands[2].is_temporary_furiten)

    def test_temp_no_furiten_after_own_nonwait_discard(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=30))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertFalse(round._hands[2].is_temporary_furiten)

    def test_temp_furiten_on_own_wait_discard(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        round.do_action(
            2, OpenCallAction(action_type=ActionType.CHII, other_tiles=(51, 61))
        )
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=192))
        self.assertSetEqual(round._hands[2].waits, {19})
        self.assertTrue(round._hands[2].is_temporary_furiten)

    def test_temp_furiten_after_call(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.CHII, other_tiles=(80, 90))
        )
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertTrue(round._hands[2].is_temporary_furiten)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertTrue(round._hands[2].is_temporary_furiten)

    def test_temp_no_furiten_after_closed_kan(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, ClosedKanAction(tiles=(70, 71, 72, 73)))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertFalse(round._hands[2].is_temporary_furiten)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertFalse(round._hands[2].is_temporary_furiten)

    def test_temp_furiten_after_added_kan(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(40, 41))
        )
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=30))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=261))
        round.do_action(3, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=262))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(
            0,
            AddKanAction(
                tile=42,
                pon_call=OpenCall(
                    call_type=CallType.PON,
                    called_player_index=1,
                    called_tile=43,
                    other_tiles=(40, 41),
                ),
            ),
        )
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertFalse(round._hands[2].is_temporary_furiten)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertTrue(round._hands[2].is_temporary_furiten)


class RiichiFuritenTest(unittest.TestCase):
    def start_round_and_riichi(self) -> Round:
        round = Round(tiles=test_deck_furiten, options=GameOptions(allow_riichi=True))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=191))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=260))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.RIICHI, tile=30))
        round.do_action(3, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=261))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        return round

    def test_riichi_no_furiten_on_discard(self) -> None:
        round = self.start_round_and_riichi()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertFalse(round._hands[2].is_riichi_furiten)

    def test_riichi_furiten_after_discard(self) -> None:
        round = self.start_round_and_riichi()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.assertTrue(round._hands[2].is_riichi_furiten)

    def test_riichi_furiten_after_second_discard(self) -> None:
        round = self.start_round_and_riichi()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        self.assertTrue(round._hands[2].is_riichi_furiten)

    def test_riichi_furiten_after_own_nonwait_discard(self) -> None:
        round = self.start_round_and_riichi()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=270))
        self.assertTrue(round._hands[2].is_riichi_furiten)

    def test_riichi_furiten_on_own_wait_discard(self) -> None:
        round = Round(tiles=test_deck_furiten, options=GameOptions(allow_riichi=True))
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=190))
        self.assertSetEqual(round._hands[0].waits, {19})
        self.assertTrue(round._hands[0].is_riichi_furiten)

    def test_riichi_furiten_after_call(self) -> None:
        round = self.start_round_and_riichi()
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.CHII, other_tiles=(80, 90))
        )
        self.assertTrue(round._hands[2].is_riichi_furiten)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        self.assertTrue(round._hands[2].is_riichi_furiten)

    def test_riichi_no_furiten_after_closed_kan(self) -> None:
        round = self.start_round_and_riichi()
        round.do_action(0, ClosedKanAction(tiles=(70, 71, 72, 73)))
        self.assertFalse(round._hands[2].is_riichi_furiten)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.assertFalse(round._hands[2].is_riichi_furiten)

    def test_riichi_furiten_after_added_kan(self) -> None:
        round = Round(tiles=test_deck_furiten, options=GameOptions(allow_riichi=True))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(40, 41))
        )
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=30))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.RIICHI, tile=261))
        round.do_action(3, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=262))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(
            0,
            AddKanAction(
                tile=42,
                pon_call=OpenCall(
                    call_type=CallType.PON,
                    called_player_index=1,
                    called_tile=43,
                    other_tiles=(40, 41),
                ),
            ),
        )
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertFalse(round._hands[2].is_riichi_furiten)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertTrue(round._hands[2].is_riichi_furiten)


class OwnDiscardFuritenTest(unittest.TestCase):
    def test_own_discard_no_furiten_on_discard(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=30))
        self.assertSetEqual(round._hands[2].waits, {4, 7})
        self.assertFalse(round._hands[2].is_own_discard_furiten)

    def test_own_discard_furiten_on_discard(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        self.assertSetEqual(round._hands[0].waits, {4, 7, 19})
        self.assertTrue(round._hands[0].is_own_discard_furiten)

    def test_own_discard_furiten_after_discard(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.assertSetEqual(round._hands[0].waits, {4, 7, 19})
        self.assertTrue(round._hands[0].is_own_discard_furiten)

    def test_own_discard_furiten_after_call(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.CHII, other_tiles=(80, 90))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        self.assertSetEqual(round._hands[0].waits, {4, 7, 19})
        self.assertTrue(round._hands[0].is_own_discard_furiten)

    def test_own_discard_no_furiten_after_closed_kan(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, ClosedKanAction(tiles=(70, 71, 72, 73)))
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        self.assertSetEqual(round._hands[0].waits, {4, 19})
        self.assertFalse(round._hands[0].is_own_discard_furiten)

    def test_own_discard_no_furiten_after_added_kan(self) -> None:
        round = Round(tiles=test_deck_furiten)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=70))
        round.do_action(
            1, OpenCallAction(action_type=ActionType.CHII, other_tiles=(80, 90))
        )
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=43))
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(40, 41))
        )
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=310))
        round.do_action(
            3, OpenCallAction(action_type=ActionType.PON, other_tiles=(311, 312))
        )
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=210))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(
            0,
            AddKanAction(
                tile=42,
                pon_call=OpenCall(
                    call_type=CallType.PON,
                    called_player_index=1,
                    called_tile=43,
                    other_tiles=(40, 41),
                ),
            ),
        )
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=60))
        round.display_info()
        self.assertSetEqual(round._hands[0].waits, {1})
        self.assertFalse(round._hands[0].is_own_discard_furiten)
