import unittest

from src.mahjong.win import Win
from src.mahjong.game_options import GameOptions
from src.mahjong.scoring import Scorer


class ScoringTest(unittest.TestCase):
    def get_player_scores(self, win: Win) -> list[float]:
        return Scorer.score(win, GameOptions()).player_scores

    def test_dealer_ron(self) -> None:
        win = Win(
            win_player=0,
            lose_player=1,
            hand=[30, 31, 40, 41, 90, 91, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [12.0, -12.0, 0.0, 0.0])

    def test_dealer_tsumo(self) -> None:
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[30, 31, 40, 41, 90, 91, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [24.0, -8.0, -8.0, -8.0])

    def test_nondealer_ron(self) -> None:
        win = Win(
            win_player=2,
            lose_player=1,
            hand=[30, 31, 40, 41, 90, 91, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [0.0, -8.0, 8.0, 0.0])

    def test_nondealer_tsumo(self) -> None:
        win = Win(
            win_player=2,
            lose_player=None,
            hand=[30, 31, 40, 41, 90, 91, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [-8.0, -4.0, 16.0, -4.0])

    def test_sub_round_dealer_tsumo(self) -> None:
        win = Win(
            win_player=1,
            lose_player=None,
            hand=[30, 31, 40, 41, 90, 91, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=1,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [-8.0, 24.0, -8.0, -8.0])

    def test_sub_round_nondealer_ron(self) -> None:
        win = Win(
            win_player=0,
            lose_player=1,
            hand=[30, 31, 40, 41, 90, 91, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=1,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [8.0, -8.0, 0.0, 0.0])
