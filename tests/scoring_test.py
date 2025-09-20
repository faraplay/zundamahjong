import unittest

from src.mahjong.call import Call, CallType
from src.mahjong.yaku import Win
from src.mahjong.game_options import GameOptions
from src.mahjong.scoring import Scorer


class ScoringTest(unittest.TestCase):
    def get_player_scores(self, win: Win):
        return Scorer.score(win, GameOptions()).player_scores

    def test_dealer_ron(self):
        win = Win(
            win_player=0,
            lose_player=1,
            hand=[12, 13, 16, 17, 36, 37, 60, 61, 84, 85, 88, 89, 124, 125],
            calls=[],
            flowers=[168],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [12.0, -12.0, 0.0, 0.0])

    def test_dealer_tsumo(self):
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[12, 13, 16, 17, 36, 37, 60, 61, 84, 85, 88, 89, 124, 125],
            calls=[],
            flowers=[168],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [24.0, -8.0, -8.0, -8.0])

    def test_nondealer_ron(self):
        win = Win(
            win_player=2,
            lose_player=1,
            hand=[12, 13, 16, 17, 36, 37, 60, 61, 84, 85, 88, 89, 124, 125],
            calls=[],
            flowers=[168],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [0.0, -8.0, 8.0, 0.0])

    def test_nondealer_tsumo(self):
        win = Win(
            win_player=2,
            lose_player=None,
            hand=[12, 13, 16, 17, 36, 37, 60, 61, 84, 85, 88, 89, 124, 125],
            calls=[],
            flowers=[168],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [-8.0, -4.0, 16.0, -4.0])

    def test_sub_round_dealer_tsumo(self):
        win = Win(
            win_player=1,
            lose_player=None,
            hand=[12, 13, 16, 17, 36, 37, 60, 61, 84, 85, 88, 89, 124, 125],
            calls=[],
            flowers=[168],
            player_count=4,
            wind_round=0,
            sub_round=1,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [-8.0, 24.0, -8.0, -8.0])

    def test_sub_round_nondealer_ron(self):
        win = Win(
            win_player=0,
            lose_player=1,
            hand=[12, 13, 16, 17, 36, 37, 60, 61, 84, 85, 88, 89, 124, 125],
            calls=[],
            flowers=[168],
            player_count=4,
            wind_round=0,
            sub_round=1,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [8.0, -8.0, 0.0, 0.0])
