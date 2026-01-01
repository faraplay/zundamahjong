from unittest import TestCase
from .get_pattern_mults import get_pattern_mults

from zundamahjong.mahjong.call import ClosedKanCall
from zundamahjong.mahjong.meld import Meld, MeldType


class NoCallsTest(TestCase):
    def test_no_calls_tsumo(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "NO_CALLS": 1,
                "NO_CALLS_TSUMO": 1,
            },
        )

    def test_no_calls_tsumo_closed_kan(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
            ],
            calls=[
                ClosedKanCall(tiles=(190, 191, 192, 193)),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_QUAD": 1,
                "NON_PINFU_TSUMO": 1,
                "NO_CALLS": 1,
                "NO_CALLS_TSUMO": 1,
            },
        )

    def test_no_calls_ron(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NO_CALLS_RON": 1,
                "NO_CALLS": 1,
            },
        )

    def test_no_calls_ron_closed_kan(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
            ],
            calls=[
                ClosedKanCall(tiles=(190, 191, 192, 193)),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_QUAD": 1,
                "NO_CALLS_RON": 1,
                "NO_CALLS": 1,
            },
        )
