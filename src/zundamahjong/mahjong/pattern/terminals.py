from ..tile import is_number, terminals
from .pattern_calculator import PatternCalculator, register_pattern
from .wait_pattern import WaitPattern


@register_pattern(
    "ALL_SIMPLES",
    display_name="All Simples",
    han=1,
    fu=0,
)
def all_simples(self: PatternCalculator) -> int:
    return int(
        all((is_number(tile) and 2 <= tile % 10 <= 8) for tile in self.hand_tiles)
    )


@register_pattern(
    "HALF_OUTSIDE_HAND",
    display_name="Half Outside Hand",
    han=2,
    fu=0,
)
def half_outside_hand(self: PatternCalculator) -> int:
    return int(self.call_outsidenesses == {1, 2})


@register_pattern(
    "FULLY_OUTSIDE_HAND",
    display_name="Fully Outside Hand",
    han=4,
    fu=0,
)
def fully_outside_hand(self: PatternCalculator) -> int:
    return int(self.call_outsidenesses == {2})


@register_pattern(
    "ALL_TERMINALS_AND_HONOURS",
    display_name="All Terminals and Honours",
    han=3,
    fu=0,
)
def all_terminals_and_honours(self: PatternCalculator) -> int:
    return int(
        len(self.chii_start_tiles) == 0
        and half_outside_hand(self)
        and not (thirteen_orphans(self) or thirteen_orphans_13_sided_wait(self))
    )


@register_pattern(
    "ALL_TERMINALS",
    display_name="All Terminals",
    han=13,
    fu=0,
)
def all_terminals(self: PatternCalculator) -> int:
    return int(all(tile in terminals for tile in self.hand_tiles))


@register_pattern(
    "THIRTEEN_ORPHANS",
    display_name="Thirteen Orphans",
    han=13,
    fu=0,
)
def thirteen_orphans(self: PatternCalculator) -> int:
    return int(self.wait_pattern == WaitPattern.KOKUSHI)


@register_pattern(
    "THIRTEEN_ORPHANS_13_SIDED_WAIT",
    display_name="Thirteen Orphans 13-sided Wait",
    han=13,
    fu=0,
)
def thirteen_orphans_13_sided_wait(self: PatternCalculator) -> int:
    return int(self.wait_pattern == WaitPattern.KOKUSHI_13)
