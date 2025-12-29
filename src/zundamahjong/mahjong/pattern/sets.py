from .pattern_calculator import PatternCalculator, register_pattern
from .wait_pattern import WaitPattern


@register_pattern(
    "ALL_TRIPLETS",
    display_name="All Triplets",
    han=3,
    fu=0,
)
def all_triplets(self: PatternCalculator) -> int:
    return int(len(self.triplet_tiles) == 4)


@register_pattern(
    "TRIPLE_TRIPLETS",
    display_name="Triple Triplets",
    han=4,
    fu=0,
)
def triple_triplets(self: PatternCalculator) -> int:
    return int(
        any(
            {tile, tile + 10, tile + 20} <= self.triplet_tiles
            for tile in self.triplet_tiles
            if tile < 10
        )
    )


@register_pattern(
    "THREE_CONCEALED_TRIPLETS",
    display_name="Three Concealed Triplets",
    han=3,
    fu=0,
)
def three_concealed_triplets(self: PatternCalculator) -> int:
    return int(self.concealed_triplets == 3)


@register_pattern(
    "FOUR_CONCEALED_TRIPLETS",
    display_name="Four Concealed Triplets",
    han=12,
    fu=0,
)
def four_concealed_triplets(self: PatternCalculator) -> int:
    return int(
        self.concealed_triplets == 4 and self.wait_pattern == WaitPattern.SHANPON
    )


@register_pattern(
    "FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT",
    display_name="Four Concealed Triplets 1-sided Wait",
    han=12,
    fu=0,
)
def four_concealed_triplets_1_sided_wait(self: PatternCalculator) -> int:
    return int(self.concealed_triplets == 4 and self.wait_pattern == WaitPattern.TANKI)


@register_pattern(
    "THREE_QUADS",
    display_name="Three Quads",
    han=4,
    fu=0,
)
def three_quads(self: PatternCalculator) -> int:
    return int(self.quads == 3)


@register_pattern(
    "FOUR_QUADS",
    display_name="Four Quads",
    han=18,
    fu=0,
)
def four_quads(self: PatternCalculator) -> int:
    return int(self.quads == 4)
