import unittest

from src.mahjong.call import Call, CallType
from src.mahjong.win_info import Win
from src.mahjong.game_options import GameOptions
from src.mahjong.scoring import ScoringHand


class ScoringTest(unittest.TestCase):

    def get_yaku_hans(self, win: Win):
        return ScoringHand(win, GameOptions()).get_win_scoring().scoring.yaku_hans

    def test_eyes(self):
        win = Win(
            win_seat=0,
            lose_seat=None,
            hand=[8, 8, 19, 19, 19],
            calls=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        yaku_hans = self.get_yaku_hans(win)
        self.assertDictEqual(yaku_hans, {"EYES": 1})

    def test_all_runs(self):
        win = Win(
            win_seat=0,
            lose_seat=None,
            hand=[1, 1],
            calls=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[14, 15, 16]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        yaku_hans = self.get_yaku_hans(win)
        self.assertDictEqual(yaku_hans, {"ALL_RUNS": 1})

    def test_all_simples(self):
        win = Win(
            win_seat=0,
            lose_seat=None,
            hand=[3, 3, 3, 4, 5, 6, 23, 23],
            calls=[
                Call(call_type=CallType.PON, tiles=[15, 15, 15]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        yaku_hans = self.get_yaku_hans(win)
        self.assertDictEqual(yaku_hans, {"ALL_SIMPLES": 1})
