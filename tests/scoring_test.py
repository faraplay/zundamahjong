import unittest

from src.mahjong.call import Call, CallType
from src.mahjong.yaku import Win
from src.mahjong.game_options import GameOptions
from src.mahjong.scoring import ScoringHand


class ScoringTest(unittest.TestCase):
    def get_seat_scores(self, win: Win):
        return ScoringHand(win, GameOptions()).get_win_scoring().scoring.seat_scores

    def test_dealer_ron(self):
        win = Win(
            win_seat=0,
            lose_seat=1,
            hand=[3, 3, 4, 4, 9, 9, 15, 15, 21, 21, 22, 22, 31, 31],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            wind_round=0,
        )
        seat_scores = self.get_seat_scores(win)
        self.assertSequenceEqual(seat_scores, [12.0, -12.0, 0.0, 0.0])

    def test_dealer_tsumo(self):
        win = Win(
            win_seat=0,
            lose_seat=None,
            hand=[3, 3, 4, 4, 9, 9, 15, 15, 21, 21, 22, 22, 31, 31],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            wind_round=0,
        )
        seat_scores = self.get_seat_scores(win)
        self.assertSequenceEqual(seat_scores, [36.0, -12.0, -12.0, -12.0])

    def test_nondealer_ron(self):
        win = Win(
            win_seat=2,
            lose_seat=1,
            hand=[3, 3, 4, 4, 9, 9, 15, 15, 21, 21, 22, 22, 31, 31],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            wind_round=0,
        )
        seat_scores = self.get_seat_scores(win)
        self.assertSequenceEqual(seat_scores, [0.0, -8.0, 8.0, 0.0])

    def test_nondealer_tsumo(self):
        win = Win(
            win_seat=2,
            lose_seat=None,
            hand=[3, 3, 4, 4, 9, 9, 15, 15, 21, 21, 22, 22, 31, 31],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            wind_round=0,
        )
        seat_scores = self.get_seat_scores(win)
        self.assertSequenceEqual(seat_scores, [-8.0, -4.0, 16.0, -4.0])
