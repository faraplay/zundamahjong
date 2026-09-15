from pydantic import BaseModel

from .pattern import PatternData, default_pattern_data


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
    min_yaku: int = 0
    "The minimum number of han needed in a winning hand (not counting dora)."

    allow_riichi: bool = True
    "Whether to allow riichi."

    riichi_cost: float = 1000.0
    "The amount of points it costs to riichi."

    can_riichi_negative_score: bool = True
    "Allow riichi even if it the player would have a negative score."

    allow_rob_added_kan: bool = True
    "Whether to allow robbing added kans."

    allow_thirteen_orphans_rob_closed_kan: bool = True
    "Whether to allow robbing closed kans to form thirteen orphans."

    allow_rob_closed_kan: bool = False
    "Whether to allow robbing closed kans."

    use_temporary_furiten: bool = True
    """
    Whether to use temporary furiten.

    If this is active, players cannot ron if any of their waits
    has been discarded since their last discard.
    """
    use_riichi_furiten: bool = True
    """
    Whether to use riichi furiten.

    If this is active, players who have riichi'd cannot ron if any of their waits
    has been discarded since they called riichi.
    """
    use_own_discard_furiten: bool = True
    """
    Whether to use own-discard furiten.

    If this is active, players cannot ron if any of their waits
    were discarded by themselves earlier.
    """

    end_last_round_if_dealer_ahead: bool = False
    """
    Whether to end the game if it is the last round and the
    dealer has the highest score (even if it should be a dealer repeat).
    """

    show_waits: bool = True
    "Whether to show waits in the client UI."
    show_shanten_info: bool = False
    "Whether to show the shanten and useful tiles in the client UI."

    max_kan_count: int = 4
    "The maximum number of kans allowed in a round."
    max_dora_count: int = 5
    "The maximum number of dora indicators to reveal in a round."
    start_dora_count: int = 1
    "The number of dora indicators revealed at the start of a round."
    dead_wall_additional_tiles: int = 0
    """
    The number of extra tiles in the dead wall, in addition to the dora
    indicators and tiles needed for kan/flowers.
    """

    @property
    def true_max_dora_count(self) -> int:
        "The calculated maximum number of dora indicators to reveal in a round."
        return max(
            min(
                self.max_dora_count,
                self.max_kan_count + self.start_dora_count,
            ),
            self.start_dora_count,
        )

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

    calculate_fu: bool = True
    """
    Whether to calculate fu in score calculation.

    If this is set to ``False``, all winning hands will use the
    :py:attr:`base_fu` as the total fu in the score calculation.
    """
    base_fu: int = 20
    """
    The base amount of fu that any winning hand starts with.
    """
    round_up_fu: bool = False
    """
    Whether to round up the total fu to the next multiple of 10.
    """
    seven_pairs_use_fixed_fu: bool = True
    """
    Whether a seven-pairs hand should score a fixed amount of fu.
    """
    seven_pairs_fixed_fu: int = 25
    """
    The amount of fu a seven-pairs hand will score, if the option to score
    a fixed amount of fu for a seven-pairs hand is enabled.
    """
    round_up_points: bool = False
    """
    Whether to round up the total points each losing player plays to the next
    multiple of 100.
    """

    base_score_limits: list[ScoreLimit] = [
        ScoreLimit(han=6, score=6400.0),
        ScoreLimit(han=10, score=12800.0),
    ]
    """
    A list of limit hans and their corresponding base scores.

    The base score of a hand is calculated by the formula

    .. math::
       \\text{base score} = (\\text{total fu}) \\times 4
       \\times 2^{(\\text{total han})} .

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
