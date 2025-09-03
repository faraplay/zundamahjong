from unittest import TestCase

from src.mahjong.call import Call, CallType
from src.mahjong.yaku import Win
from src.mahjong.yaku import YakuCalculator


class YakuTest(TestCase):

    def get_yaku_mults(
        self,
        *,
        win_seat: int = 0,
        lose_seat: int | None = None,
        formed_hand: list[Call],
        calls: list[Call],
    ):
        win = Win(
            win_seat=win_seat,
            lose_seat=lose_seat,
            hand=[tile for call in formed_hand for tile in call.tiles],
            calls=calls,
        )
        return YakuCalculator(win, formed_hand).get_yaku_mults()

    def test_eyes(self):
        yaku_mults = self.get_yaku_mults(
            win_seat=0,
            lose_seat=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[8, 8]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"EYES": 1})

    def test_all_runs(self):
        yaku_mults = self.get_yaku_mults(
            win_seat=0,
            lose_seat=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[1, 1]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[14, 15, 16]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"ALL_RUNS": 1})

    def test_all_simples(self):
        yaku_mults = self.get_yaku_mults(
            win_seat=0,
            lose_seat=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[3, 3, 3]),
                Call(call_type=CallType.CHI, tiles=[4, 5, 6]),
                Call(call_type=CallType.PAIR, tiles=[23, 23]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[15, 15, 15]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"ALL_SIMPLES": 1})

    def test_seven_pairs(self):
        yaku_mults = self.get_yaku_mults(
            win_seat=0,
            lose_seat=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[3, 3]),
                Call(call_type=CallType.PAIR, tiles=[4, 4]),
                Call(call_type=CallType.PAIR, tiles=[9, 9]),
                Call(call_type=CallType.PAIR, tiles=[15, 15]),
                Call(call_type=CallType.PAIR, tiles=[21, 21]),
                Call(call_type=CallType.PAIR, tiles=[22, 22]),
                Call(call_type=CallType.PAIR, tiles=[31, 31]),
            ],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"SEVEN_PAIRS": 1})
