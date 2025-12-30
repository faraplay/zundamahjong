from typing import Any
from unittest import TestCase

from zundamahjong.mahjong.call import (
    AddKanCall,
    Call,
    CallType,
    ClosedKanCall,
    OpenCall,
    OpenKanCall,
)
from zundamahjong.mahjong.meld import Meld, MeldType
from zundamahjong.mahjong.pattern import get_pattern_mults
from zundamahjong.mahjong.tile import TileId
from zundamahjong.mahjong.win import Win


def get_pattern_mults_test(
    *,
    win_player: int = 0,
    lose_player: int | None,
    formed_hand: list[Meld],
    calls: list[Call],
    flowers: list[TileId],
    player_count: int = 4,
    wind_round: int = 0,
    sub_round: int = 0,
    **kwargs: Any,  # pyright: ignore[reportAny, reportExplicitAny]
) -> dict[str, int]:
    hand = [tile for meld in formed_hand for tile in meld.tiles]
    winning_melds = [
        meld for meld in formed_hand if meld.winning_tile_index is not None
    ]
    assert len(winning_melds) == 1
    winning_meld = winning_melds[0]
    assert winning_meld.winning_tile_index is not None
    winning_tile = winning_meld.tiles[winning_meld.winning_tile_index]
    hand.remove(winning_tile)
    hand.append(winning_tile)
    win = Win(
        win_player=win_player,
        lose_player=lose_player,
        hand=hand,
        calls=calls,
        flowers=flowers,
        player_count=player_count,
        wind_round=wind_round,
        sub_round=sub_round,
        **kwargs,  # pyright: ignore[reportAny]
    )
    return get_pattern_mults(win, formed_hand)


class PatternTest(TestCase):
    def test_open_wait(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
        pattern_mults = get_pattern_mults_test(
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
        pattern_mults = get_pattern_mults_test(
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
        pattern_mults = get_pattern_mults_test(
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
        pattern_mults = get_pattern_mults_test(
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
        pattern_mults = get_pattern_mults_test(
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

    def test_no_flowers(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            flowers=[],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NO_FLOWERS": 1,
            },
        )

    def test_player_flower(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            flowers=[410],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 1,
            },
        )

    def test_sub_round_player_flower(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            sub_round=1,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 1,
            },
        )

    def test_two_player_flowers(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            flowers=[410, 450],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 2,
            },
        )

    def test_set_of_flowers(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            flowers=[410, 420, 430, 440],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 1,
                "SET_OF_FLOWERS": 1,
            },
        )

    def test_seven_flowers(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            flowers=[410, 420, 430, 440, 460, 470, 480],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 1,
                "SET_OF_FLOWERS": 1,
                "SEVEN_FLOWERS": 1,
            },
        )

    def test_two_sets_of_flowers(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            flowers=[410, 420, 430, 440, 450, 460, 470, 480],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 2,
                "TWO_SETS_OF_FLOWERS": 1,
            },
        )

    def test_draw(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            draw_count=1,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "DRAW": 1,
            },
        )

    def test_after_a_flower(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            after_flower_count=1,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "AFTER_A_FLOWER": 1,
            },
        )

    def test_after_a_kan(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            after_kan_count=1,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "AFTER_A_KAN": 1,
            },
        )

    def test_player_wind(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[320, 321, 322]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=0,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "SEAT_WIND": 1,
            },
        )

    def test_sub_round_player_wind(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=2,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[320, 321, 322]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=1,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[440],
            sub_round=1,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "SEAT_WIND": 1,
            },
        )

    def test_prevalent_wind(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[310, 311, 312]),
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
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "PREVALENT_WIND": 1,
            },
        )

    def test_white_dragon(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[350, 351, 352]),
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
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "WHITE_DRAGON": 1,
            },
        )

    def test_green_dragon(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[360, 361, 362]),
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
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "GREEN_DRAGON": 1,
            },
        )

    def test_red_dragon(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[370, 371, 372]),
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
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "RED_DRAGON": 1,
            },
        )

    def test_eyes(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.PON, tiles=[190, 191, 192], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.PAIR, tiles=[80, 81]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=10,
                    other_tiles=(20, 30),
                ),
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=150,
                    other_tiles=(160, 170),
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
                "DUAL_PON_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "EYES": 1,
            },
        )

    def test_no_calls(self) -> None:
        pattern_mults = get_pattern_mults_test(
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

    def test_no_calls_tsumo(self) -> None:
        pattern_mults = get_pattern_mults_test(
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

    def test_no_calls_closed_kan(self) -> None:
        pattern_mults = get_pattern_mults_test(
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

    def test_no_calls_tsumo_closed_kan(self) -> None:
        pattern_mults = get_pattern_mults_test(
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

    def test_chankan(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=1,
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
            is_chankan=True,
        )
        self.assertDictEqual(
            pattern_mults,
            {"OPEN_WAIT": 1, "ORPHAN_CLOSED_TRIPLET": 1, "ROBBING_A_KAN": 1},
        )

    def test_haitei(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            is_haitei=True,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "UNDER_THE_SEA": 1,
            },
        )

    def test_houtei(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
            is_houtei=True,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "UNDER_THE_RIVER": 1,
            },
        )

    def test_all_sequences(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PAIR, tiles=[10, 11], winning_tile_index=0),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=12,
                    other_tiles=(20, 30),
                ),
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
            pattern_mults, {"PAIR_WAIT": 1, "NON_PINFU_TSUMO": 1, "ALL_SEQUENCES": 1}
        )

    def test_all_simples(self) -> None:
        pattern_mults = get_pattern_mults_test(
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

    def test_pure_straight(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.CHI, tiles=[240, 250, 260]),
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
                "PURE_STRAIGHT": 1,
            },
        )

    def test_all_triplets(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(231, 232),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "SIMPLE_OPEN_TRIPLET": 1,
                "ORPHAN_OPEN_TRIPLET": 1,
                "SIMPLE_CLOSED_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "ALL_TRIPLETS": 1,
            },
        )

    def test_half_flush(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
        pattern_mults = get_pattern_mults_test(
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

    def test_seven_pairs(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PAIR, tiles=[30, 31], winning_tile_index=0),
                Meld(meld_type=MeldType.PAIR, tiles=[40, 41]),
                Meld(meld_type=MeldType.PAIR, tiles=[90, 91]),
                Meld(meld_type=MeldType.PAIR, tiles=[150, 151]),
                Meld(meld_type=MeldType.PAIR, tiles=[210, 211]),
                Meld(meld_type=MeldType.PAIR, tiles=[220, 221]),
                Meld(meld_type=MeldType.PAIR, tiles=[310, 311]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(pattern_mults, {"SEVEN_PAIRS": 1})

    def test_half_outside_hand(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
        pattern_mults = get_pattern_mults_test(
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

    def test_pure_double_sequence(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[11, 21, 31]),
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
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "PURE_DOUBLE_SEQUENCE": 1,
            },
        )

    def test_twice_pure_double_sequence(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[11, 21, 31]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=241,
                    other_tiles=(231, 251),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "OPEN_PINFU": 1,
                "NON_PINFU_TSUMO": 1,
                "ALL_SEQUENCES": 1,
                "TWICE_PURE_DOUBLE_SEQUENCE": 1,
            },
        )

    def test_pure_triple_sequence(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[11, 21, 31]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[240, 241]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=12,
                    other_tiles=(22, 32),
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
                "PURE_TRIPLE_SEQUENCE": 1,
            },
        )

    def test_pure_quadruple_sequence(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[11, 21, 31]),
                Meld(meld_type=MeldType.CHI, tiles=[13, 23, 33]),
                Meld(meld_type=MeldType.PAIR, tiles=[240, 241]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=12,
                    other_tiles=(22, 32),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "OPEN_PINFU": 1,
                "NON_PINFU_TSUMO": 1,
                "ALL_SEQUENCES": 1,
                "PURE_QUADRUPLE_SEQUENCE": 1,
            },
        )

    def test_mixed_triple_sequence(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[30, 40, 50], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[130, 140, 150]),
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
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "MIXED_TRIPLE_SEQUENCE": 1,
            },
        )

    def test_three_concealed_triplets(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
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
            {
                "PAIR_WAIT": 1,
                "SIMPLE_CLOSED_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "THREE_CONCEALED_TRIPLETS": 1,
            },
        )

    def test_three_quads(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.CHI, tiles=[110, 120, 130], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
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
                ClosedKanCall(tiles=(190, 191, 192, 193)),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "SIMPLE_OPEN_QUAD": 1,
                "ORPHAN_OPEN_QUAD": 1,
                "ORPHAN_CLOSED_QUAD": 1,
                "NON_PINFU_TSUMO": 1,
                "THREE_QUADS": 1,
            },
        )

    def test_triple_triplets(self) -> None:
        pattern_mults = get_pattern_mults_test(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[90, 91, 92], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
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
                "ORPHAN_OPEN_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "NON_PINFU_TSUMO": 1,
                "TRIPLE_TRIPLETS": 1,
            },
        )

    def test_all_terminals_and_honours(self) -> None:
        pattern_mults = get_pattern_mults_test(
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
