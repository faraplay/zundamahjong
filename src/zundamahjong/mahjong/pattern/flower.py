from .pattern import PatternCalculator, register_pattern


@register_pattern(
    "NO_FLOWERS",
    display_name="No Flowers",
    han=1,
    fu=0,
)
def no_flowers(self: PatternCalculator) -> int:
    return int(len(self.flowers) == 0)


@register_pattern(
    "SEAT_FLOWER",
    display_name="Seat Flower",
    han=1,
    fu=0,
)
def player_flower(self: PatternCalculator) -> int:
    return sum((tile - 41) % 4 == self.seat for tile in self.flowers)


@register_pattern(
    "SET_OF_FLOWERS",
    display_name="Set of Flowers",
    han=2,
    fu=0,
)
def set_of_flowers(self: PatternCalculator) -> int:
    if self.win.player_count == 3:
        return int(
            (({41, 42, 43} <= self.flowers) + ({45, 46, 47} <= self.flowers)) == 1
        )
    else:
        return int(
            (({41, 42, 43, 44} <= self.flowers) + ({45, 46, 47, 48} <= self.flowers))
            == 1
        )


@register_pattern(
    "FIVE_FLOWERS",
    display_name="Five Flowers",
    han=2,
    fu=0,
)
def five_flowers(self: PatternCalculator) -> int:
    return int(self.win.player_count == 3 and len(self.flowers) == 5)


@register_pattern(
    "SEVEN_FLOWERS",
    display_name="Seven Flowers",
    han=2,
    fu=0,
)
def seven_flowers(self: PatternCalculator) -> int:
    return int(len(self.flowers) == 7)


@register_pattern(
    "TWO_SETS_OF_FLOWERS",
    display_name="Two Sets of Flowers",
    han=8,
    fu=0,
)
def two_sets_of_flowers(self: PatternCalculator) -> int:
    if self.win.player_count == 3:
        return int(len(self.flowers) == 6)
    else:
        return int(len(self.flowers) == 8)
