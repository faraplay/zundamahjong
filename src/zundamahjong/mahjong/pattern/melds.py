from .pattern import register_pattern, PatternCalculator


@register_pattern(
    "SIMPLE_OPEN_TRIPLET",
    display_name="Simple Open Triplet",
    han=0,
    fu=2,
)
def simple_open_triplet(self: PatternCalculator) -> int:
    return self.simple_open_triplet_count


@register_pattern(
    "ORPHAN_OPEN_TRIPLET",
    display_name="Orphan Open Triplet",
    han=0,
    fu=4,
)
def orphan_open_triplet(self: PatternCalculator) -> int:
    return self.orphan_open_triplet_count


@register_pattern(
    "SIMPLE_CLOSED_TRIPLET",
    display_name="Simple Closed Triplet",
    han=0,
    fu=4,
)
def simple_closed_triplet(self: PatternCalculator) -> int:
    return self.simple_closed_triplet_count


@register_pattern(
    "ORPHAN_CLOSED_TRIPLET",
    display_name="Orphan Closed Triplet",
    han=0,
    fu=8,
)
def orphan_closed_triplet(self: PatternCalculator) -> int:
    return self.orphan_closed_triplet_count


@register_pattern(
    "SIMPLE_OPEN_QUAD",
    display_name="Simple Open Quad",
    han=0,
    fu=8,
)
def simple_open_quad(self: PatternCalculator) -> int:
    return self.simple_open_quad_count


@register_pattern(
    "ORPHAN_OPEN_QUAD",
    display_name="Orphan Open Quad",
    han=0,
    fu=16,
)
def orphan_open_quad(self: PatternCalculator) -> int:
    return self.orphan_open_quad_count


@register_pattern(
    "SIMPLE_CLOSED_QUAD",
    display_name="Simple Closed Quad",
    han=0,
    fu=16,
)
def simple_closed_quad(self: PatternCalculator) -> int:
    return self.simple_closed_quad_count


@register_pattern(
    "ORPHAN_CLOSED_QUAD",
    display_name="Orphan Closed Quad",
    han=0,
    fu=32,
)
def orphan_closed_quad(self: PatternCalculator) -> int:
    return self.orphan_closed_quad_count
