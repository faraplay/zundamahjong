from ..win import Win
from ..meld import Meld

from .pattern import pattern_mult_funcs, PatternCalculator

from . import melds


def get_pattern_mults(win: Win, formed_hand: list[Meld]) -> dict[str, int]:
    pattern_mults: dict[str, int] = {}
    pattern_calculator = PatternCalculator(win, formed_hand)
    for pattern, get_pattern_multiplicity in pattern_mult_funcs.items():
        pattern_mult = get_pattern_multiplicity(pattern_calculator)
        if pattern_mult != 0:
            pattern_mults[pattern] = pattern_mult
    return pattern_mults
