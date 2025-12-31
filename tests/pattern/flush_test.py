from unittest import TestCase
from .get_pattern_mults import get_pattern_mults

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.meld import Meld, MeldType


class FlushTest(TestCase):
    def test_half_flush(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[50, 60, 70]),
                Meld(meld_type=MeldType.PON, tiles=[90, 91, 92]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=31,
                    other_tiles=(40, 51),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "HALF_FLUSH": 1,
            },
        )

    def test_full_flush(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[50, 60, 70]),
                Meld(meld_type=MeldType.PON, tiles=[90, 91, 92]),
                Meld(meld_type=MeldType.PAIR, tiles=[31, 32]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=33,
                    other_tiles=(40, 51),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "FULL_FLUSH": 1,
            },
        )

    def test_nine_gates(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[20, 30, 40]),
                Meld(meld_type=MeldType.CHI, tiles=[41, 50, 60]),
                Meld(meld_type=MeldType.CHI, tiles=[70, 80, 90]),
                Meld(meld_type=MeldType.PAIR, tiles=[91, 92]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 1,
                "NO_CALLS_RON": 1,
                "NO_CALLS": 1,
                "FULL_FLUSH": 1,
                "NINE_GATES": 1,
            },
        )

    def test_true_nine_gates(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
                Meld(meld_type=MeldType.CHI, tiles=[20, 30, 40]),
                Meld(meld_type=MeldType.CHI, tiles=[41, 50, 60], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[70, 80, 90]),
                Meld(meld_type=MeldType.PAIR, tiles=[91, 92]),
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
                "FULL_FLUSH": 1,
                "TRUE_NINE_GATES": 1,
            },
        )

    def test_full_flush_not_nine_gates(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[50, 60, 70]),
                Meld(meld_type=MeldType.PON, tiles=[90, 91, 92]),
                Meld(meld_type=MeldType.PAIR, tiles=[31, 32]),
                Meld(meld_type=MeldType.CHI, tiles=[33, 40, 51]),
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
                "FULL_FLUSH": 1,
            },
        )

    def test_all_greens(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.CHI, tiles=[220, 230, 240], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.PON, tiles=[231, 232, 233]),
                Meld(meld_type=MeldType.CHI, tiles=[280, 281, 282]),
                Meld(meld_type=MeldType.PAIR, tiles=[360, 361]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=260,
                    other_tiles=(261, 262),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "SIMPLE_OPEN_TRIPLET": 1,
                "SIMPLE_CLOSED_TRIPLET": 1,
                "YAKUHAI_PAIR": 1,
                "NON_PINFU_TSUMO": 1,
                "HALF_FLUSH": 1,
                "ALL_GREENS": 1,
            },
        )
