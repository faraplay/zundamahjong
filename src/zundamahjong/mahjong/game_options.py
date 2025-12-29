from pydantic import BaseModel

from .pattern.pattern import PatternData, default_pattern_data


class ScoreLimit(BaseModel):
    "Represents a limit amount of han and the corresponding base score."

    han: int
    score: float


class GameOptions(BaseModel):
    """
    Holds various options for a game of mahjong.
    """

    player_count: int = 4
    "The number of players."
    game_length_wind_rounds: int = 1
    "The number of wind rounds to play."
    game_length_sub_rounds: int = 0
    "The number of sub rounds to play (in addition to the full wind rounds)."
    use_flowers: bool = True
    "Whether to use flower tiles."
    auto_replace_flowers: bool = True
    "Whether to automatically replace flowers."
    end_wall_count: int = 14
    "The number of tiles left in the wall for an exhaustive draw."
    min_han: int = 0
    "The minimum number of han needed in a winning hand."

    allow_riichi: bool = False
    "Whether to allow riichi."

    show_waits: bool = True
    "Whether to show waits in the client UI."
    show_shanten_info: bool = False
    "Whether to show the shanten and useful tiles in the client UI."

    start_score: float = 0.0
    "The score each player starts with at the start of the game."
    score_dealer_ron_multiplier: float = 6.0
    """
    The losing player deals in the *base score* multiplied by this
    if they deal in to the dealer.
    """
    score_dealer_tsumo_multiplier: float = 2.0
    """
    Losing players deal in the *base score* multiplied by this
    if the dealer wins by tsumo.
    """
    score_nondealer_ron_multiplier: float = 4.0
    """
    The losing player deals in the *base score* multiplied by this
    if they deal in to a nondealer.
    """
    score_nondealer_tsumo_nondealer_multiplier: float = 1.0
    """
    Losing nondealer players deal in the *base score* multiplied by this
    if a nondealer wins by tsumo.
    """
    score_nondealer_tsumo_dealer_multiplier: float = 2.0
    """
    The dealer deals in the *base score* multiplied by this
    if a nondealer wins by tsumo.
    """

    calculate_fu: bool = False
    """
    Whether to calculate fu in score calculation.

    If this is set to ``False``, all winning hands will use the
    :py:attr:`base_fu` as the total fu in the score calculation.
    """
    base_fu: int = 25
    """
    The base amount of fu that any winning hand starts with.
    """
    round_up_fu: bool = False
    """
    Whether to round up the total fu to the next multiple of 10.
    """
    round_up_points: bool = False
    """
    Whether to round up the total points each losing player plays to the next
    multiple of 100.
    """

    base_score_limits: list[ScoreLimit] = [ScoreLimit(han=6, score=6400.0)]
    """
    A list of limit hans and their corresponding base scores.

    The base score of a hand is calculated by the formula
        :math:`\\text{base score} = (\\text{total fu}) \\times 4
        \\times 2^{(\\text{total han})}` .

    If this list is empty, then no base score caps will be applied.

    If a hand with a lower han value than the smallest han value on this list
    would score more than the smallest base score in this list, its base score
    is capped at the smallest base score in this list.

    If a hand has han value greater than or equal to some han value on this list,
    then its base score is set to the base score of the entry with the greatest
    han value that is less than or equal to the hand's han value.
    If this is tied among multiple entries, the one with the
    largest base score is used.
    """

    pattern_data: dict[str, PatternData] = default_pattern_data
    """
    A dictionary of all possible patterns,
    with the han and fu that each of them score.
    If a pattern's han and fu are set to zero, then the pattern will not
    be used in the game's scoring.

    Patterns are indexed by the internal names of the patterns
    (in SCREAMING_SNAKE_CASE).
    """

    @property
    def game_length(self) -> tuple[int, int]:
        return (self.game_length_wind_rounds, self.game_length_sub_rounds)
