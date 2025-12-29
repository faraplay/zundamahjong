# ruff: noqa: I001

# These are imported in order to register their functions.
from . import (
    special_win,  # noqa: F401
    sequences,  # noqa: F401
    pinfu,  # noqa: F401
    sets,  # noqa: F401
    pairs,  # noqa: F401
    flush,  # noqa: F401
    terminals,  # noqa: F401
    honours,  # noqa: F401
    yakuhai,  # noqa: F401
    melds,  # noqa: F401
    no_calls,  # noqa: F401
    flower,  # noqa: F401
    wait,  # noqa: F401
)

from .pattern import PatternData as PatternData
from .pattern import default_pattern_data as default_pattern_data


from ..meld import Meld
from ..win import Win
from .pattern import pattern_mult_funcs, PatternCalculator


def get_pattern_mults(win: Win, formed_hand: list[Meld]) -> dict[str, int]:
    pattern_mults: dict[str, int] = {}
    pattern_calculator = PatternCalculator(win, formed_hand)
    for pattern, get_pattern_multiplicity in pattern_mult_funcs.items():
        pattern_mult = get_pattern_multiplicity(pattern_calculator)
        if pattern_mult != 0:
            pattern_mults[pattern] = pattern_mult
    return pattern_mults
