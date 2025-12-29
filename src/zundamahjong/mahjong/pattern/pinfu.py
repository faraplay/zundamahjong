from .wait_pattern import WaitPattern
from .pattern import register_pattern, PatternCalculator
from .yakuhai import yakuhaipair


@register_pattern(
    "PINFU",
    display_name="Pinfu",
    han=0,
    fu=0,
)
def pinfu(self: PatternCalculator) -> int:
    return int(
        len(self.win.calls) == 0
        and self.chii_meld_count == 4
        and self.wait_pattern == WaitPattern.RYANMEN
        and not yakuhaipair(self)
    )


@register_pattern(
    "OPEN_PINFU",
    display_name="Open Pinfu",
    han=0,
    fu=2,
)
def open_pinfu(self: PatternCalculator) -> int:
    return int(
        len(self.win.calls) != 0
        and self.chii_meld_count == 4
        and self.wait_pattern == WaitPattern.RYANMEN
        and not yakuhaipair(self)
    )


@register_pattern(
    "NON_PINFU_TSUMO",
    display_name="Non Pinfu Tsumo",
    han=0,
    fu=2,
)
def non_pinfu_tsumo(self: PatternCalculator) -> int:
    return int(self.win.lose_player is None and not pinfu(self))
