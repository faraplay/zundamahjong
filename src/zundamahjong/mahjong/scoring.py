from math import ceil
from typing import final

from pydantic import BaseModel

from .form_hand import formed_hand_possibilities
from .game_options import GameOptions
from .meld import Meld
from .pattern.pattern import PatternCalculator, PatternData, default_pattern_data
from .win import Win


class Scoring(BaseModel):
    """
    Represents the score data associated to a win in a round of mahjong.
    """

    win_player: int
    "The index of the winning player."
    lose_player: int | None
    "The index of the player who dealt in, or ``None`` if the win was tsumo."
    patterns: dict[str, PatternData]
    """
    A dictionary containing the :py:class:`PatternData` for the patterns
    that the hand has.

    Patterns are indexed by the internal names of the patterns
    (in SCREAMING_SNAKE_CASE).
    """
    han: int
    "The total han value of the hand."
    fu: int
    "The total fu value of the hand."
    player_scores: list[float]
    "The amount of points each player wins or loses from this hand."


def _round_up_int(value: int, step: int) -> int:
    return step * ceil(value / step)


def _round_up_float(value: float, step: float) -> float:
    return step * ceil(value / step)


@final
class Scorer:
    """
    Class to calculate the score from a :py:class:`Win` object.

    Objects in this class should not be instantiated directly;
    instead, use the :py:meth:`score` class method.
    """

    def __init__(self, win: Win, options: GameOptions) -> None:
        self._win = win
        self._options = options
        self._low_han_max_score = min(
            (score_limit.score for score_limit in self._options.base_score_limits),
            default=None,
        )
        self._pattern_data = default_pattern_data | options.pattern_data

    def _get_limit_base_score(self, han: int) -> float | None:
        best_score_limit = max(
            (
                (score_limit.han, score_limit.score)
                for score_limit in self._options.base_score_limits
                if score_limit.han <= han
            ),
            default=None,
        )
        return best_score_limit[1] if best_score_limit is not None else None

    def _get_player_scores(self, han: int, fu: int) -> list[float]:
        player_count = self._options.player_count
        win_player = self._win.win_player
        lose_player = self._win.lose_player
        limit_base_score = self._get_limit_base_score(han)
        if limit_base_score is None:
            han_multiplier = 1 << han
            base_score: float = fu * 4 * han_multiplier
            if self._low_han_max_score is not None:
                base_score = min(base_score, self._low_han_max_score)
        else:
            base_score = limit_base_score
        if lose_player is None:
            if win_player == self._win.sub_round:
                player_pay_in_amount = (
                    self._options.score_dealer_tsumo_multiplier * base_score
                )
                if self._options.round_up_points:
                    player_pay_in_amount = _round_up_float(player_pay_in_amount, 100)
                player_scores = [-player_pay_in_amount] * player_count
                player_scores[win_player] = player_pay_in_amount * (player_count - 1)
            else:
                player_pay_in_amount = (
                    self._options.score_nondealer_tsumo_nondealer_multiplier
                    * base_score
                )
                if self._options.round_up_points:
                    player_pay_in_amount = _round_up_float(player_pay_in_amount, 100)
                dealer_pay_in_amount = (
                    self._options.score_nondealer_tsumo_dealer_multiplier * base_score
                )
                if self._options.round_up_points:
                    dealer_pay_in_amount = _round_up_float(dealer_pay_in_amount, 100)
                player_scores = [-player_pay_in_amount] * player_count
                player_scores[self._win.sub_round] = -dealer_pay_in_amount
                player_scores[win_player] = (
                    player_count - 2
                ) * player_pay_in_amount + dealer_pay_in_amount
        else:
            if win_player == self._win.sub_round:
                player_pay_in_amount = (
                    self._options.score_dealer_ron_multiplier * base_score
                )
            else:
                player_pay_in_amount = (
                    self._options.score_nondealer_ron_multiplier * base_score
                )
            if self._options.round_up_points:
                player_pay_in_amount = _round_up_float(player_pay_in_amount, 100)
            player_scores = [0.0] * player_count
            player_scores[win_player] = player_pay_in_amount
            player_scores[lose_player] = -player_pay_in_amount
        return player_scores

    def _get_formed_hand_scoring(self, formed_hand: list[Meld]) -> Scoring:
        pattern_mults = PatternCalculator(self._win, formed_hand).get_pattern_mults()
        patterns = [
            (
                pattern,
                PatternData(
                    display_name=pattern_data.display_name,
                    han=pattern_data.han * pattern_mults[pattern],
                    fu=pattern_data.fu * pattern_mults[pattern],
                ),
            )
            for pattern, pattern_data in self._pattern_data.items()
            if pattern in pattern_mults
        ]
        han = sum(pattern_data.han for (_, pattern_data) in patterns)
        if self._options.calculate_fu:
            fu = self._options.base_fu + sum(
                pattern_data.fu for (_, pattern_data) in patterns
            )
        else:
            fu = self._options.base_fu
        if self._options.round_up_fu:
            fu = _round_up_int(fu, 10)
        player_scores = self._get_player_scores(han, fu)
        if self._options.calculate_fu:
            patterns_dict = dict(
                (pattern, pattern_data)
                for (pattern, pattern_data) in patterns
                if pattern_data.han != 0 or pattern_data.fu != 0
            )
        else:
            patterns_dict = dict(
                (pattern, pattern_data)
                for (pattern, pattern_data) in patterns
                if pattern_data.han != 0
            )
        return Scoring(
            win_player=self._win.win_player,
            lose_player=self._win.lose_player,
            patterns=patterns_dict,
            han=han,
            fu=fu,
            player_scores=player_scores,
        )

    def _get_scoring(self) -> Scoring:
        scorings = [
            self._get_formed_hand_scoring(formed_hand)
            for formed_hand in formed_hand_possibilities(self._win.hand)
        ]

        def key(scoring: Scoring) -> tuple[float, int, int]:
            return (
                scoring.player_scores[self._win.win_player],
                scoring.han,
                scoring.fu,
            )

        return max(scorings, key=key)

    @classmethod
    def score(cls, win: Win, options: GameOptions) -> Scoring:
        """
        Calculate the score a winning hand should get.

        :param win: The :py:class:`Win` object to calculate the score for.
        :param options: The :py:class:`GameOptions` object to use when scoring.
        :return: A :py:class:`Scoring` object containing the scoring data.
        """
        return cls(win, options)._get_scoring()
