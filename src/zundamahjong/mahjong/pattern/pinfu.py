from .pattern_calculator import PatternCalculator, register_pattern
from .wait_pattern import WaitPattern
from .yakuhai import yakuhaipair


def _pinfu(self: PatternCalculator) -> bool:
    return (
        self.chii_meld_count == 4
        and self.wait_pattern == WaitPattern.RYANMEN
        and not yakuhaipair(self)
    )


@register_pattern(
    "CLOSED_PINFU",
    display_name="Pinfu",
    han=0,
    fu=0,
)
def closed_pinfu(self: PatternCalculator) -> int:
    """
    All four melds are sequences, the wait pattern is an open wait,
    the pair is not a yakuhai tile, and the hand is closed.
    """
    return int(_pinfu(self) and self.is_closed_hand)


@register_pattern(
    "OPEN_PINFU",
    display_name="Open Pinfu",
    han=0,
    fu=2,
)
def open_pinfu(self: PatternCalculator) -> int:
    """
    All four melds are sequences, the wait pattern is an open wait,
    the pair is not a yakuhai tile, and the hand is open.
    """
    return int(_pinfu(self) and not self.is_closed_hand)


@register_pattern(
    "NON_PINFU_TSUMO",
    display_name="Non Pinfu Tsumo",
    han=0,
    fu=2,
)
def non_pinfu_tsumo(self: PatternCalculator) -> int:
    """
    The winning tile was drawn by the player, and the hand does not
    qualify for pinfu.
    """
    return int(self.win.lose_player is None and not _pinfu(self))
