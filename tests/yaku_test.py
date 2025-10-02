from typing import Optional

from unittest import TestCase

from src.mahjong.tile import TileId
from src.mahjong.meld import Meld, MeldType
from src.mahjong.call import Call, CallType, ClosedKanCall, OpenCall
from src.mahjong.yaku import Win
from src.mahjong.yaku import YakuCalculator


def get_yaku_mults(
    *,
    win_player: int = 0,
    lose_player: Optional[int],
    formed_hand: list[Meld],
    calls: list[Call],
    flowers: list[TileId],
    player_count: int = 4,
    wind_round: int = 0,
    sub_round: int = 0,
    **kwargs
):
    win = Win(
        win_player=win_player,
        lose_player=lose_player,
        hand=[tile for meld in formed_hand for tile in meld.tiles],
        calls=calls,
        flowers=flowers,
        player_count=player_count,
        wind_round=wind_round,
        sub_round=sub_round,
        **kwargs
    )
    return YakuCalculator(win, formed_hand).get_yaku_mults()


class YakuTest(TestCase):
    def test_no_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"NO_FLOWERS": 1})

    def test_player_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1})

    def test_sub_round_player_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1})

    def test_two_player_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 2})

    def test_set_of_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1, "SET_OF_FLOWERS": 1})

    def test_seven_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults, {"SEAT_FLOWER": 1, "SET_OF_FLOWERS": 1, "SEVEN_FLOWERS": 1}
        )

    def test_two_sets_of_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"SEAT_FLOWER": 2, "TWO_SETS_OF_FLOWERS": 1},
        )

    def test_draw(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"DRAW": 1},
        )

    def test_after_a_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"AFTER_A_FLOWER": 1},
        )

    def test_after_a_kan(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"AFTER_A_KAN": 1},
        )

    def test_player_wind(self):
        yaku_mults = get_yaku_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"SEAT_WIND": 1},
        )

    def test_sub_round_player_wind(self):
        yaku_mults = get_yaku_mults(
            win_player=2,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"SEAT_WIND": 1},
        )

    def test_prevalent_wind(self):
        yaku_mults = get_yaku_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"PREVALENT_WIND": 1},
        )

    def test_white_dragon(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"WHITE_DRAGON": 1},
        )

    def test_green_dragon(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"GREEN_DRAGON": 1},
        )

    def test_red_dragon(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"RED_DRAGON": 1},
        )

    def test_eyes(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
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
        self.assertDictEqual(yaku_mults, {"EYES": 1})

    def test_no_calls(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1})

    def test_no_calls_closed_kan(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
            ],
            calls=[
                ClosedKanCall(tiles=(190, 191, 192, 193)),
            ],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1})

    def test_chankan(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"ROBBING_A_KAN": 1})

    def test_haitei(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"UNDER_THE_SEA": 1})

    def test_houtei(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"UNDER_THE_RIVER": 1})

    def test_all_runs(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PAIR, tiles=[10, 11]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=12,
                    other_tiles=(0, 30),
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
        self.assertDictEqual(yaku_mults, {"ALL_RUNS": 1})

    def test_all_simples(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[30, 31, 32]),
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
        self.assertDictEqual(yaku_mults, {"ALL_SIMPLES": 1})

    def test_pure_straight(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[210, 220, 230]),
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
        self.assertDictEqual(yaku_mults, {"PURE_STRAIGHT": 1})

    def test_all_triplets(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
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
        self.assertDictEqual(yaku_mults, {"ALL_TRIPLETS": 1})

    def test_half_flush(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"HALF_FLUSH": 1})

    def test_full_flush(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
        self.assertDictEqual(yaku_mults, {"FULL_FLUSH": 1})

    def test_seven_pairs(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PAIR, tiles=[30, 31]),
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
        self.assertDictEqual(yaku_mults, {"SEVEN_PAIRS": 1})

    def test_half_outside_hand(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"HALF_OUTSIDE_HAND": 1},
        )

    def test_fully_outside_hand(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"FULLY_OUTSIDE_HAND": 1},
        )

    def test_pure_double_sequence(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
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
            yaku_mults,
            {"PURE_DOUBLE_SEQUENCE": 1},
        )

    def test_twice_pure_double_sequence(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.CHI, tiles=[11, 21, 31]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=231,
                    other_tiles=(241, 251),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            yaku_mults,
            {"ALL_RUNS": 1, "TWICE_PURE_DOUBLE_SEQUENCE": 1},
        )

    def test_mixed_triple_sequence(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[30, 40, 50]),
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
            yaku_mults,
            {"MIXED_TRIPLE_SEQUENCE": 1},
        )

    def test_triple_triplets(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[90, 91, 92]),
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
            yaku_mults,
            {"TRIPLE_TRIPLETS": 1},
        )

    def test_all_terminals_and_honours(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
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
            yaku_mults,
            {"HALF_OUTSIDE_HAND": 1, "ALL_TRIPLETS": 1, "ALL_TERMINALS_AND_HONOURS": 1},
        )
