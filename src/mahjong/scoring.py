from typing import Optional

from pydantic import BaseModel

from .meld import Meld
from .win import Win
from .yaku import YakuCalculator, yaku_display_names
from .game_options import GameOptions
from .form_hand import formed_hand_possibilities


class Scoring(BaseModel):
    win_player: int
    lose_player: Optional[int]
    yaku_hans: dict[str, int]
    han_total: int
    player_scores: list[float]


class Scorer:
    def __init__(self, win: Win, options: GameOptions):
        self._win = win
        self._options = options

    def _get_player_scores(self, han_total: int):
        player_count = self._options.player_count
        win_player = self._win.win_player
        lose_player = self._win.lose_player
        han_multiplier: int = 2 ** min(han_total, 6)
        if lose_player is None:
            if win_player == self._win.sub_round:
                player_pay_in_amount = (
                    self._options.score_dealer_tsumo_base_value * han_multiplier
                )
                player_scores = [-player_pay_in_amount] * player_count
                player_scores[win_player] = player_pay_in_amount * (player_count - 1)
            else:
                player_pay_in_amount = (
                    self._options.score_nondealer_tsumo_nondealer_base_value
                    * han_multiplier
                )
                dealer_pay_in_amount = (
                    self._options.score_nondealer_tsumo_dealer_base_value
                    * han_multiplier
                )
                player_scores = [-player_pay_in_amount] * player_count
                player_scores[0] = -dealer_pay_in_amount
                player_scores[win_player] = (
                    player_count - 2
                ) * player_pay_in_amount + dealer_pay_in_amount
        else:
            if win_player == self._win.sub_round:
                player_pay_in_amount = (
                    self._options.score_dealer_ron_base_value * han_multiplier
                )
            else:
                player_pay_in_amount = (
                    self._options.score_nondealer_ron_base_value * han_multiplier
                )
            player_scores = [0.0] * player_count
            player_scores[win_player] = player_pay_in_amount
            player_scores[lose_player] = -player_pay_in_amount
        return player_scores

    def _get_formed_hand_scoring(self, formed_hand: list[Meld]):
        yaku_mults = YakuCalculator(self._win, formed_hand).get_yaku_mults()
        yaku_values = self._options.yaku_values
        yaku_hans = dict(
            (yaku_display_names[yaku], yaku_values[yaku] * yaku_mults[yaku])
            for yaku in yaku_mults.keys()
            if yaku_values[yaku] != 0
        )
        han_total = sum(yaku_hans.values())
        player_scores = self._get_player_scores(han_total)
        return Scoring(
            win_player=self._win.win_player,
            lose_player=self._win.lose_player,
            yaku_hans=yaku_hans,
            han_total=han_total,
            player_scores=player_scores,
        )

    def _get_scoring(self):
        scorings = [
            self._get_formed_hand_scoring(formed_hand)
            for formed_hand in formed_hand_possibilities(self._win.hand)
        ]

        def key(scoring: Scoring):
            return (scoring.han_total, scoring.player_scores[self._win.win_player])

        return max(scorings, key=key)

    @classmethod
    def score(cls, win, options):
        return cls(win, options)._get_scoring()
