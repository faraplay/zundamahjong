from unittest import TestCase

from tests.yaku_test import get_pattern_mults
from zundamahjong.mahjong.call import (
    AddKanCall,
    CallType,
    ClosedKanCall,
    OpenCall,
    OpenKanCall,
)
from zundamahjong.mahjong.meld import Meld, MeldType


class YakumanTest(TestCase):
    def test_blessing_of_heaven(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[],
            flowers=[420],
            is_tenhou=True,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NO_CALLS": 1,
                "NO_CALLS_TSUMO": 1,
                "BLESSING_OF_HEAVEN": 1,
            },
        )

    def test_blessing_of_earth(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[],
            flowers=[430],
            is_chiihou=True,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NO_CALLS": 1,
                "NO_CALLS_TSUMO": 1,
                "BLESSING_OF_EARTH": 1,
            },
        )

    def test_little_three_dragons(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[350, 351, 352]),
                Meld(meld_type=MeldType.PON, tiles=[230, 231, 232]),
                Meld(meld_type=MeldType.PAIR, tiles=[360, 361]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=370,
                    other_tiles=(371, 372),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "WHITE_DRAGON": 1,
                "RED_DRAGON": 1,
                "LITTLE_THREE_DRAGONS": 1,
            },
        )

    def test_big_three_dragons(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[350, 351, 352]),
                Meld(meld_type=MeldType.PON, tiles=[360, 361, 362]),
                Meld(meld_type=MeldType.PAIR, tiles=[230, 231]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=370,
                    other_tiles=(371, 372),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "WHITE_DRAGON": 1,
                "GREEN_DRAGON": 1,
                "RED_DRAGON": 1,
                "BIG_THREE_DRAGONS": 1,
            },
        )

    def test_four_little_winds(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[20, 30, 40], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PON, tiles=[340, 341, 342]),
                Meld(meld_type=MeldType.PAIR, tiles=[310, 311]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=320,
                    other_tiles=(321, 322),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "HALF_FLUSH": 1,
                "FOUR_LITTLE_WINDS": 1,
            },
        )

    def test_four_big_winds(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(
                    meld_type=MeldType.PON, tiles=[310, 311, 312], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PON, tiles=[340, 341, 342]),
                Meld(meld_type=MeldType.PAIR, tiles=[30, 31]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=320,
                    other_tiles=(321, 322),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "SEAT_WIND": 1,
                "PREVALENT_WIND": 1,
                "HALF_FLUSH": 1,
                "ALL_TRIPLETS": 1,
                "FOUR_BIG_WINDS": 1,
            },
        )

    def test_four_concealed_triplets(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
                Meld(meld_type=MeldType.PON, tiles=[230, 231, 232]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                ClosedKanCall(
                    call_type=CallType.CLOSED_KAN, tiles=(190, 191, 192, 193)
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "NO_CALLS": 1,
                "NO_CALLS_TSUMO": 1,
                "ALL_TRIPLETS": 1,
                "FOUR_CONCEALED_TRIPLETS": 1,
            },
        )

    def test_one_open_triplet(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
                Meld(meld_type=MeldType.PON, tiles=[230, 231, 232]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                ClosedKanCall(
                    call_type=CallType.CLOSED_KAN, tiles=(190, 191, 192, 193)
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "NO_CALLS": 1,
                "ALL_TRIPLETS": 1,
                "THREE_CONCEALED_TRIPLETS": 1,
            },
        )

    def test_four_concealed_triplets_1_sided_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
                Meld(meld_type=MeldType.PON, tiles=[230, 231, 232]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331], winning_tile_index=0),
            ],
            calls=[
                ClosedKanCall(
                    call_type=CallType.CLOSED_KAN, tiles=(190, 191, 192, 193)
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "PAIR_WAIT": 1,
                "NO_CALLS": 1,
                "ALL_TRIPLETS": 1,
                "FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT": 1,
            },
        )

    def test_all_honours(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(
                    meld_type=MeldType.PON, tiles=[360, 361, 362], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PON, tiles=[340, 341, 342]),
                Meld(meld_type=MeldType.PAIR, tiles=[350, 351]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=320,
                    other_tiles=(321, 322),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "GREEN_DRAGON": 1,
                "ALL_TRIPLETS": 1,
                "ALL_HONOURS": 1,
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
            pattern_mults, {"OPEN_WAIT": 1, "HALF_FLUSH": 1, "ALL_GREENS": 1}
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
        self.assertDictEqual(pattern_mults, {"THIRTEEN_ORPHANS": 1})

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
        self.assertDictEqual(pattern_mults, {"THIRTEEN_ORPHANS_13_SIDED_WAIT": 1})

    def test_four_quads(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331], winning_tile_index=0),
            ],
            calls=[
                OpenKanCall(
                    called_player_index=0, called_tile=10, other_tiles=(11, 12, 13)
                ),
                AddKanCall(
                    called_player_index=0,
                    called_tile=150,
                    added_tile=151,
                    other_tiles=(152, 153),
                ),
                AddKanCall(
                    called_player_index=0,
                    called_tile=230,
                    added_tile=231,
                    other_tiles=(232, 233),
                ),
                ClosedKanCall(tiles=(190, 191, 192, 193)),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults, {"PAIR_WAIT": 1, "ALL_TRIPLETS": 1, "FOUR_QUADS": 1}
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
            {"DUAL_PON_WAIT": 1, "NO_CALLS": 1, "FULL_FLUSH": 1, "NINE_GATES": 1},
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
            {"OPEN_WAIT": 1, "NO_CALLS": 1, "FULL_FLUSH": 1, "TRUE_NINE_GATES": 1},
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
            pattern_mults, {"OPEN_WAIT": 1, "NO_CALLS": 1, "FULL_FLUSH": 1}
        )
