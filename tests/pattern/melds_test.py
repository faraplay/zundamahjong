from unittest import TestCase

from zundamahjong.mahjong.call import CallType, ClosedKanCall, OpenCall, OpenKanCall
from zundamahjong.mahjong.meld import Meld, MeldType

from .get_pattern_mults import get_pattern_mults


class MeldsTest(TestCase):
    def test_simple_open_triplet(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=180,
                    other_tiles=(181, 182),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "SIMPLE_OPEN_TRIPLET": 1},
        )

    def test_orphan_open_triplet(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=190,
                    other_tiles=(191, 192),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_OPEN_TRIPLET": 1},
        )

    def test_simple_closed_triplet(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[180, 181, 182]),
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
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "SIMPLE_CLOSED_TRIPLET": 1},
        )

    def test_orphan_closed_triplet(self) -> None:
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
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_CLOSED_TRIPLET": 1},
        )

    def test_simple_open_quad(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
                OpenKanCall(
                    called_player_index=3,
                    called_tile=180,
                    other_tiles=(181, 182, 183),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "SIMPLE_OPEN_QUAD": 1},
        )

    def test_orphan_open_quad(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
                OpenKanCall(
                    called_player_index=3,
                    called_tile=190,
                    other_tiles=(191, 192, 193),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_OPEN_QUAD": 1},
        )

    def test_simple_closed_quad(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
                ClosedKanCall(
                    tiles=(180, 181, 182, 183),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "SIMPLE_CLOSED_QUAD": 1},
        )

    def test_orphan_closed_quad(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
                ClosedKanCall(
                    tiles=(190, 191, 192, 193),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "NON_PINFU_TSUMO": 1, "ORPHAN_CLOSED_QUAD": 1},
        )
