from unittest import TestCase

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.meld import Meld, MeldType

from .get_pattern_mults import get_pattern_mults


class WaitTest(TestCase):
    def test_open_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_CLOSED_TRIPLET": 1},
        )

    def test_closed_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=1),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {"CLOSED_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_CLOSED_TRIPLET": 1},
        )

    def test_low_edge_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=2),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {"EDGE_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_CLOSED_TRIPLET": 1},
        )

    def test_high_edge_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[70, 80, 90], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {"EDGE_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_CLOSED_TRIPLET": 1},
        )

    def test_dual_pon_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(
                    meld_type=MeldType.PON, tiles=[190, 191, 192], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {"DUAL_PON_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_CLOSED_TRIPLET": 1},
        )

    def test_pair_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331], winning_tile_index=0),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {"PAIR_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_CLOSED_TRIPLET": 1},
        )
