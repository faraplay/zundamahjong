from ..tile import is_number
from .pattern_calculator import PatternCalculator, register_pattern


@register_pattern(
    "SEVEN_PAIRS",
    display_name="Seven Pairs",
    han=3,
    fu=0,
)
def sevenpairs(self: PatternCalculator) -> int:
    """
    The hand consists of seven different pairs (this is a special hand structure).
    """
    return int(self.pair_count == 7)


@register_pattern(
    "EYES",
    display_name="Eyes",
    han=1,
    fu=0,
)
def eyes(self: PatternCalculator) -> int:
    """
    The hand's pair is a 2, 5 or 8.
    """
    if self.pair_count != 1:
        return 0
    tile = self.pair_tile
    if not is_number(tile):
        return 0
    return int((tile % 10) % 3 == 2)
