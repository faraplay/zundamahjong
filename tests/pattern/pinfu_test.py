from unittest import TestCase
from .get_pattern_mults import get_pattern_mults

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.meld import Meld, MeldType


class PinfuTest(TestCase):
    def test_closed_pinfu(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[140, 150, 160]),
                Meld(meld_type=MeldType.CHI, tiles=[151, 161, 170]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NO_CALLS": 1,
                "NO_CALLS_TSUMO": 1,
                "CLOSED_PINFU": 1,
                "ALL_SEQUENCES": 1,
            },
        )

    def test_open_pinfu(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=140,
                    other_tiles=(150, 160),
                ),
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=151,
                    other_tiles=(161, 170),
                ),
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
            {
                "OPEN_WAIT": 1,
                "OPEN_PINFU": 1,
                "ALL_SEQUENCES": 1,
            },
        )

    def test_non_pinfu_tsumo(self) -> None:
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
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
            },
        )
