from .pattern_calculator import PatternCalculator, register_pattern


@register_pattern(
    "BLESSING_OF_HEAVEN",
    display_name="Blessing of Heaven",
    han=20,
    fu=0,
)
def blessing_of_heaven(self: PatternCalculator) -> int:
    return int(self.win.is_tenhou)


@register_pattern(
    "BLESSING_OF_EARTH",
    display_name="Blessing of Earth",
    han=19,
    fu=0,
)
def blessing_of_earth(self: PatternCalculator) -> int:
    return int(self.win.is_chiihou)


@register_pattern(
    "RIICHI",
    display_name="Riichi",
    han=1,
    fu=0,
)
def riichi(self: PatternCalculator) -> int:
    return int(self.win.is_riichi and not self.win.is_double_riichi)


@register_pattern(
    "DOUBLE_RIICHI",
    display_name="Double Riichi",
    han=2,
    fu=0,
)
def double_riichi(self: PatternCalculator) -> int:
    return int(self.win.is_double_riichi)


@register_pattern(
    "IPPATSU",
    display_name="Ippatsu",
    han=1,
    fu=0,
)
def ippatsu(self: PatternCalculator) -> int:
    return int(self.win.is_ippatsu)


@register_pattern(
    "ROBBING_A_KAN",
    display_name="Robbing a Kan",
    han=1,
    fu=0,
)
def robbing_a_kan(self: PatternCalculator) -> int:
    return int(self.win.is_chankan)


@register_pattern(
    "UNDER_THE_SEA",
    display_name="Under the Sea",
    han=1,
    fu=0,
)
def under_the_sea(self: PatternCalculator) -> int:
    return int(self.win.is_haitei)


@register_pattern(
    "UNDER_THE_RIVER",
    display_name="Under the River",
    han=1,
    fu=0,
)
def under_the_river(self: PatternCalculator) -> int:
    return int(self.win.is_houtei)


@register_pattern(
    "AFTER_A_FLOWER",
    display_name="After a Flower",
    han=1,
    fu=0,
)
def after_a_flower(self: PatternCalculator) -> int:
    return self.win.after_flower_count


@register_pattern(
    "AFTER_A_KAN",
    display_name="After a Kan",
    han=2,
    fu=0,
)
def after_a_kan(self: PatternCalculator) -> int:
    return self.win.after_kan_count


@register_pattern(
    "DRAW",
    display_name="Draw",
    han=1,
    fu=0,
)
def draw(self: PatternCalculator) -> int:
    return self.win.draw_count
