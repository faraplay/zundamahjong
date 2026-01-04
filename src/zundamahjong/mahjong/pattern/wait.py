from .pattern_calculator import PatternCalculator, register_pattern
from .wait_pattern import WaitPattern


@register_pattern(
    "OPEN_WAIT",
    display_name="Open Wait",
    han=0,
    fu=0,
)
def open_wait(self: PatternCalculator) -> int:
    """
    The winning tile is on one end of a sequence, and the other end of the
    sequence is not a terminal.
    """
    return int(self.wait_pattern == WaitPattern.RYANMEN)


@register_pattern(
    "CLOSED_WAIT",
    display_name="Closed Wait",
    han=0,
    fu=2,
)
def closed_wait(self: PatternCalculator) -> int:
    """
    The winning tile is in the middle of a sequence.
    """
    return int(self.wait_pattern == WaitPattern.KANCHAN)


@register_pattern(
    "EDGE_WAIT",
    display_name="Edge Wait",
    han=0,
    fu=2,
)
def edge_wait(self: PatternCalculator) -> int:
    """
    The winning tile is on one end of a sequence, and the other end of the
    sequence is a terminal.
    """
    return int(self.wait_pattern == WaitPattern.PENCHAN)


@register_pattern(
    "DUAL_PON_WAIT",
    display_name="Dual Pon Wait",
    han=0,
    fu=0,
)
def dual_pon_wait(self: PatternCalculator) -> int:
    """
    The winning tile is part of a triplet.
    """
    return int(self.wait_pattern == WaitPattern.SHANPON)


@register_pattern(
    "PAIR_WAIT",
    display_name="Pair Wait",
    han=0,
    fu=2,
)
def pair_wait(self: PatternCalculator) -> int:
    """
    The winning tile is part of a pair.
    """
    return int(self.wait_pattern == WaitPattern.TANKI and self.pair_count == 1)
