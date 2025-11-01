import unittest

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.game_options import GameOptions
from zundamahjong.mahjong.pattern import PatternData
from zundamahjong.mahjong.scoring import Scorer
from zundamahjong.mahjong.win import Win


class ScoringTest(unittest.TestCase):
    def get_player_scores(self, win: Win) -> list[float]:
        return Scorer.score(
            win, GameOptions(player_count=win.player_count)
        ).player_scores

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
        self.assertSequenceEqual(player_scores, [1200.0, -1200.0, 0.0, 0.0])

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
        self.assertSequenceEqual(player_scores, [2400.0, -800.0, -800.0, -800.0])

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
        self.assertSequenceEqual(player_scores, [0.0, -800.0, 800.0, 0.0])

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
        self.assertSequenceEqual(player_scores, [-800.0, -400.0, 1600.0, -400.0])

    def test_sub_round_dealer_ron(self) -> None:
        win = Win(
            win_player=1,
            lose_player=0,
            hand=[30, 31, 40, 41, 90, 91, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=1,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [-1200.0, 1200.0, 0.0, 0.0])

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
        self.assertSequenceEqual(player_scores, [-800.0, 2400.0, -800.0, -800.0])

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
        self.assertSequenceEqual(player_scores, [800.0, -800.0, 0.0, 0.0])

    def test_sub_round_nondealer_tsumo(self) -> None:
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[30, 31, 40, 41, 90, 91, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=1,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [1600.0, -800.0, -400.0, -400.0])

    def test_3player_dealer_ron(self) -> None:
        win = Win(
            win_player=0,
            lose_player=1,
            hand=[90, 91, 130, 131, 140, 141, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=3,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [1200.0, -1200.0, 0.0])

    def test_3player_dealer_tsumo(self) -> None:
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[90, 91, 130, 131, 140, 141, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=3,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [1600.0, -800.0, -800.0])

    def test_3player_nondealer_ron(self) -> None:
        win = Win(
            win_player=2,
            lose_player=1,
            hand=[90, 91, 130, 131, 140, 141, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=3,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [0.0, -800.0, 800.0])

    def test_3player_nondealer_tsumo(self) -> None:
        win = Win(
            win_player=2,
            lose_player=None,
            hand=[90, 91, 130, 131, 140, 141, 150, 151, 210, 211, 220, 221, 310, 311],
            calls=[],
            flowers=[420],
            player_count=3,
            wind_round=0,
            sub_round=0,
        )
        player_scores = self.get_player_scores(win)
        self.assertSequenceEqual(player_scores, [-800.0, -400.0, 1200.0])

    def test_calculate_fu(self) -> None:
        win = Win(
            win_player=0,
            lose_player=1,
            hand=[20, 30, 150, 160, 170, 190, 191, 192, 330, 331, 10],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        scoring = Scorer.score(win, GameOptions(calculate_fu=True, base_fu=20))
        self.assertDictEqual(
            scoring.patterns,
            {
                "ORPHAN_CLOSED_TRIPLET": PatternData(
                    display_name="Orphan Closed Triplet", han=0, fu=8
                ),
            },
        )
        self.assertEqual(scoring.han, 0)
        self.assertEqual(scoring.fu, 28)
        self.assertSequenceEqual(scoring.player_scores, [168.0, -168.0, 0.0, 0.0])

    def test_fu_rounding(self) -> None:
        win = Win(
            win_player=0,
            lose_player=1,
            hand=[20, 30, 150, 160, 170, 190, 191, 192, 330, 331, 10],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        scoring = Scorer.score(
            win, GameOptions(calculate_fu=True, base_fu=20, round_up_fu=True)
        )
        self.assertDictEqual(
            scoring.patterns,
            {
                "ORPHAN_CLOSED_TRIPLET": PatternData(
                    display_name="Orphan Closed Triplet", han=0, fu=8
                ),
            },
        )
        self.assertEqual(scoring.han, 0)
        self.assertEqual(scoring.fu, 30)
        self.assertSequenceEqual(scoring.player_scores, [180.0, -180.0, 0.0, 0.0])

    def test_point_rounding(self) -> None:
        win = Win(
            win_player=0,
            lose_player=1,
            hand=[20, 30, 150, 160, 170, 190, 191, 192, 330, 331, 10],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
            player_count=4,
            wind_round=0,
            sub_round=0,
        )
        scoring = Scorer.score(
            win, GameOptions(calculate_fu=True, base_fu=20, round_up_points=True)
        )
        self.assertDictEqual(
            scoring.patterns,
            {
                "ORPHAN_CLOSED_TRIPLET": PatternData(
                    display_name="Orphan Closed Triplet", han=0, fu=8
                ),
            },
        )
        self.assertEqual(scoring.han, 0)
        self.assertEqual(scoring.fu, 28)
        self.assertSequenceEqual(scoring.player_scores, [200.0, -200.0, 0.0, 0.0])
