from unittest import TestCase

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.meld import Meld, MeldType

from .get_pattern_mults import get_pattern_mults


class TerminalsTest(TestCase):
    def test_all_simples(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[30, 31, 32], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[40, 50, 60]),
                Meld(meld_type=MeldType.PAIR, tiles=[230, 231]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=150,
                    other_tiles=(151, 152),
                ),
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=153,
                    other_tiles=(160, 170),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "SIMPLE_OPEN_TRIPLET": 1,
                "SIMPLE_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "ALL_SIMPLES": 1,
            },
        )

    def test_half_outside_hand(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[110, 120, 130]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=270,
                    other_tiles=(280, 290),
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
                "HALF_OUTSIDE_HAND": 1,
            },
        )

    def test_fully_outside_hand(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[110, 120, 130]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[290, 291]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=270,
                    other_tiles=(280, 292),
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
                "FULLY_OUTSIDE_HAND": 1,
            },
        )

    def test_all_terminals_and_honours(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[110, 111, 112]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=290,
                    other_tiles=(291, 292),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 2,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "HALF_OUTSIDE_HAND": 1,
                "ALL_TRIPLETS": 1,
                "ALL_TERMINALS_AND_HONOURS": 1,
            },
        )

    def test_all_terminals(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[110, 111, 112]),
                Meld(meld_type=MeldType.PON, tiles=[290, 291, 292]),
                Meld(meld_type=MeldType.PAIR, tiles=[210, 211]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=190,
                    other_tiles=(191, 192),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 2,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "ALL_TRIPLETS": 1,
                "FULLY_OUTSIDE_HAND": 1,
                "ALL_TERMINALS": 1,
            },
        )

    def test_thirteen_orphans(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(
                    meld_type=MeldType.THIRTEEN_ORPHANS,
                    tiles=[
                        10,
                        90,
                        110,
                        190,
                        210,
                        290,
                        310,
                        320,
                        321,
                        330,
                        340,
                        350,
                        360,
                        370,
                    ],
                    winning_tile_index=0,
                ),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(pattern_mults, {"NO_CALLS_RON": 1, "THIRTEEN_ORPHANS": 1})

    def test_thirteen_orphans_13_sided_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(
                    meld_type=MeldType.THIRTEEN_ORPHANS,
                    tiles=[
                        10,
                        90,
                        110,
                        190,
                        210,
                        290,
                        310,
                        320,
                        321,
                        330,
                        340,
                        350,
                        360,
                        370,
                    ],
                    winning_tile_index=8,
                ),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults, {"NO_CALLS_RON": 1, "THIRTEEN_ORPHANS_13_SIDED_WAIT": 1}
        )
