from ..tile import number_suits
from .pattern_calculator import PatternCalculator, register_pattern


@register_pattern(
    "ALL_SEQUENCES",
    display_name="All Sequences",
    han=1,
    fu=0,
)
def all_sequences(self: PatternCalculator) -> int:
    """
    All four melds are sequences.
    """
    return int(self.chii_meld_count == 4)


@register_pattern(
    "PURE_DOUBLE_SEQUENCE",
    display_name="Pure Double Sequence",
    han=1,
    fu=0,
)
def pure_double_sequence(self: PatternCalculator) -> int:
    """
    Hand contains one pair of identical sequences.
    """
    return int(sum(count == 2 for count in self.chii_start_tiles.values()) == 1)


@register_pattern(
    "TWICE_PURE_DOUBLE_SEQUENCE",
    display_name="Twice Pure Double Sequence",
    han=4,
    fu=0,
)
def twice_pure_double_sequence(self: PatternCalculator) -> int:
    """
    Hand contains two pairs of identical sequences.
    """
    return int(sum(count == 2 for count in self.chii_start_tiles.values()) == 2)


@register_pattern(
    "PURE_TRIPLE_SEQUENCE",
    display_name="Pure Triple Sequence",
    han=6,
    fu=0,
)
def pure_triple_sequence(self: PatternCalculator) -> int:
    """
    Hand contains three identical sequences.
    """
    return int(sum(count == 3 for count in self.chii_start_tiles.values()) == 1)


@register_pattern(
    "PURE_QUADRUPLE_SEQUENCE",
    display_name="Pure Quadruple Sequence",
    han=12,
    fu=0,
)
def pure_quadruple_sequence(self: PatternCalculator) -> int:
    """
    Hand contains four identical sequences.
    """
    return int(sum(count == 4 for count in self.chii_start_tiles.values()) == 1)


@register_pattern(
    "PURE_STRAIGHT",
    display_name="Pure Straight",
    han=3,
    fu=0,
)
def pure_straight(self: PatternCalculator) -> int:
    """
    Hand contains sequences of 123, 456, 789 in the same suit.
    """
    return int(
        any(
            {suit + 1, suit + 4, suit + 7} <= self.chii_start_tiles.keys()
            for suit in number_suits
        )
    )


@register_pattern(
    "MIXED_TRIPLE_SEQUENCE",
    display_name="Mixed Triple Sequence",
    han=2,
    fu=0,
)
def mixed_triple_sequence(self: PatternCalculator) -> int:
    """
    Hand contains three sequences of the same numbers in different suits.
    """
    return int(
        any(
            {tile, tile + 10, tile + 20} <= self.chii_start_tiles.keys()
            for tile in self.chii_start_tiles
            if tile < 10
        )
    )
