from pydantic import BaseModel

from .call import Call
from .win import Win
from .yaku import YakuCalculator
from .game_options import GameOptions
from .form_hand import formed_hand_possibilities


class Score(BaseModel):
    yaku_hans: dict[str, int]
    han_total: int
    seat_scores: list[float]


class WinScoreInfo(BaseModel):
    win: Win
    scoring: Score


class ScoringHand:
    def __init__(self, win: Win, options: GameOptions):
        self._win = win
        self._options = options

    def get_seat_scores(self, han_total: int):
        player_count = self._options.player_count
        win_seat = self._win.win_seat
        lose_seat = self._win.lose_seat
        han_multiplier = 2 ** min(han_total, 6)
        if lose_seat is None:
            if win_seat == 0:
                seat_pay_in_amount = (
                    self._options.score_dealer_tsumo_base_value * han_multiplier
                )
                seat_scores = [-seat_pay_in_amount] * player_count
                seat_scores[win_seat] = seat_pay_in_amount * (player_count - 1)
            else:
                seat_pay_in_amount = (
                    self._options.score_nondealer_tsumo_nondealer_base_value
                    * han_multiplier
                )
                dealer_pay_in_amount = (
                    self._options.score_nondealer_tsumo_dealer_base_value
                    * han_multiplier
                )
                seat_scores = [-seat_pay_in_amount] * player_count
                seat_scores[0] = -dealer_pay_in_amount
                seat_scores[win_seat] = (
                    player_count - 2
                ) * seat_pay_in_amount + dealer_pay_in_amount
        else:
            if win_seat == 0:
                seat_pay_in_amount = (
                    self._options.score_dealer_ron_base_value * han_multiplier
                )
            else:
                seat_pay_in_amount = (
                    self._options.score_nondealer_ron_base_value * han_multiplier
                )
            seat_scores = [0] * player_count
            seat_scores[win_seat] = seat_pay_in_amount
            seat_scores[lose_seat] = -seat_pay_in_amount
        return seat_scores

    def get_scoring(self, formed_hand: list[Call]):
        yakus = YakuCalculator(self, formed_hand).get_yakus()
        yaku_values = self._options.yaku_values
        yaku_hans = dict((yaku, yaku_values[yaku]) for yaku in yakus)
        han_total = sum(yaku_hans.values())
        seat_scores = self.get_seat_scores(han_total)
        return Score(yaku_hans=yaku_hans, han_total=han_total, seat_scores=seat_scores)

    def get_win_scoring(self):
        scorings = [
            self.get_scoring(formed_hand)
            for formed_hand in formed_hand_possibilities(self._win.hand)
        ]

        def score_key(score: Score):
            return (score.han_total, score.seat_scores[self._win.win_seat])

        scoring = max(scorings, key=score_key)
        return WinScoreInfo(win=self._win, scoring=scoring)
