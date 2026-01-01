from ..tile import dragons, winds
from .pattern_calculator import PatternCalculator, register_pattern


@register_pattern(
    "LITTLE_THREE_DRAGONS",
    display_name="Little Three Dragons",
    han=5,
    fu=0,
)
def little_three_dragons(self: PatternCalculator) -> int:
    """
    The hand contains two triplets or quads of dragons,
    and a pair of the third dragon.
    """
    total = 0
    for tile in dragons:
        tile_count = self.hand_tiles.count(tile)
        if tile_count == 4:
            tile_count = 3
        total += tile_count
    return int(total == 8)


@register_pattern(
    "BIG_THREE_DRAGONS",
    display_name="Big Three Dragons",
    han=8,
    fu=0,
)
def big_three_dragons(self: PatternCalculator) -> int:
    """
    The hand contains three triplets or quads of dragons.
    """
    return dragons <= self.triplet_tiles


@register_pattern(
    "FOUR_LITTLE_WINDS",
    display_name="Four Little Winds",
    han=12,
    fu=0,
)
def four_little_winds(self: PatternCalculator) -> int:
    """
    The hand contains three triplets or quads of winds,
    and a pair of the fourth wind.
    """
    total = 0
    for tile in winds:
        tile_count = self.hand_tiles.count(tile)
        if tile_count == 4:
            tile_count = 3
        total += tile_count
    return int(total == 11)


@register_pattern(
    "FOUR_BIG_WINDS",
    display_name="Four Big Winds",
    han=16,
    fu=0,
)
def four_big_winds(self: PatternCalculator) -> int:
    """
    The hand contains four triplets or quads of winds.
    """
    return int(winds <= self.triplet_tiles)


@register_pattern(
    "ALL_HONOURS",
    display_name="All Honours",
    han=10,
    fu=0,
)
def all_honours(self: PatternCalculator) -> int:
    """
    Every tile is an honour tile.
    """
    return int(self.used_suits == {self._honour_suit})
