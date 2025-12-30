from .pattern_calculator import PatternCalculator, register_pattern


@register_pattern(
    "NO_CALLS",
    display_name="No Calls",
    han=1,
    fu=0,
)
def no_calls(self: PatternCalculator) -> int:
    """
    The hand is closed.
    """
    return int(self.pair_count == 1 and self.is_closed_hand)


@register_pattern(
    "NO_CALLS_TSUMO",
    display_name="No Calls Tsumo",
    han=0,
    fu=0,
)
def no_calls_tsumo(self: PatternCalculator) -> int:
    """
    The hand is closed, and the player drew the winning tile.
    """
    return int(self.win.lose_player is None and self.is_closed_hand)


@register_pattern(
    "NO_CALLS_RON",
    display_name="No Calls Ron",
    han=0,
    fu=10,
)
def no_calls_ron(self: PatternCalculator) -> int:
    """
    The hand is closed, and the winning tile was discarded by another player.
    """
    return int(
        self.win.lose_player is not None
        and self.is_closed_hand
        and not self.pair_count == 7
    )
