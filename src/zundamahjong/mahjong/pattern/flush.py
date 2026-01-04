from collections import Counter

from ..tile import TileValue, green_tiles, honour_suit, number_suits
from .pattern_calculator import PatternCalculator, register_pattern


@register_pattern(
    "HALF_FLUSH",
    display_name="Half Flush",
    han=3,
    fu=0,
)
def half_flush(self: PatternCalculator) -> int:
    """
    The hand contains honour tiles and tiles from only one suit.
    """
    return int(len(self.used_suits) == 2 and honour_suit in self.used_suits)


@register_pattern(
    "FULL_FLUSH",
    display_name="Full Flush",
    han=7,
    fu=0,
)
def full_flush(self: PatternCalculator) -> int:
    """
    The hand contains tiles from only one suit, with no honour tiles.
    """
    return int(any(self.used_suits == {suit} for suit in number_suits))


def _get_nine_gates_last_tile(self: PatternCalculator) -> TileValue | None:
    if not self.is_closed_hand:
        return None
    if not full_flush(self):
        return None
    suit = (self.hand_tiles[0] // 10) * 10
    model_tiles = [
        suit + 1,
        suit + 1,
        suit + 1,
        suit + 2,
        suit + 3,
        suit + 4,
        suit + 5,
        suit + 6,
        suit + 7,
        suit + 8,
        suit + 9,
        suit + 9,
        suit + 9,
    ]
    tile_counter = Counter(self.hand_tiles)
    tile_counter.subtract(model_tiles)
    if len(-tile_counter) > 0:
        return None
    return next(tile_counter.elements())


@register_pattern(
    "NINE_GATES",
    display_name="Nine Gates",
    han=11,
    fu=0,
)
def nine_gates(self: PatternCalculator) -> int:
    """
    The hand contains 1112345678999 in the same suit, plus one extra tile
    of that suit, and the winning tile is not the extra tile.
    """
    nine_gates_last_tile = _get_nine_gates_last_tile(self)
    return int(
        nine_gates_last_tile is not None and nine_gates_last_tile != self.winning_tile
    )


@register_pattern(
    "TRUE_NINE_GATES",
    display_name="True Nine Gates",
    han=19,
    fu=0,
)
def true_nine_gates(self: PatternCalculator) -> int:
    """
    The hand contains 1112345678999 in the same suit, plus one extra tile
    of that suit, and the winning tile is the extra tile.
    """
    nine_gates_last_tile = _get_nine_gates_last_tile(self)
    return int(nine_gates_last_tile == self.winning_tile)


@register_pattern(
    "ALL_GREENS",
    display_name="All Greens",
    han=16,
    fu=0,
)
def all_greens(self: PatternCalculator) -> int:
    """
    The hand only uses 2s, 3s, 4s, 6s, 8s and Hatsu.
    """
    return int(all(tile in green_tiles for tile in self.hand_tiles))
