from ..meld import MeldType
from ..tile import TileValue
from .pattern_calculator import PatternCalculator, register_pattern


def _yakuhai(self: PatternCalculator, pattern_tile: TileValue) -> int:
    return int(
        any(
            (call.tiles[0] == pattern_tile and call.meld_type != MeldType.PAIR)
            for call in self.melds
        )
    )


@register_pattern(
    "SEAT_WIND",
    display_name="Seat Wind",
    han=1,
    fu=0,
)
def seat_wind(self: PatternCalculator) -> int:
    """
    The hand contains a triplet or quad of the player seat's wind.
    """
    return _yakuhai(self, self.seat + 31)


@register_pattern(
    "PREVALENT_WIND",
    display_name="Prevalent Wind",
    han=1,
    fu=0,
)
def prevalent_wind(self: PatternCalculator) -> int:
    """
    The hand contains a triplet or quad of the wind round's wind.
    """
    return _yakuhai(self, self.win.wind_round + 31)


@register_pattern(
    "NORTH_WIND",
    display_name="North Wind",
    han=1,
    fu=0,
)
def north_wind(self: PatternCalculator) -> int:
    """
    The hand contains a triplet or quad of the North wind.
    """
    return int(self.win.player_count == 3 and _yakuhai(self, 34))


@register_pattern(
    "WHITE_DRAGON",
    display_name="White Dragon",
    han=1,
    fu=0,
)
def white_dragon(self: PatternCalculator) -> int:
    """
    The hand contains a triplet or quad of the Whiteboard.
    """
    return _yakuhai(self, 35)


@register_pattern(
    "GREEN_DRAGON",
    display_name="Green Dragon",
    han=1,
    fu=0,
)
def green_dragon(self: PatternCalculator) -> int:
    """
    The hand contains a triplet or quad of the Fat Choi.
    """
    return _yakuhai(self, 36)


@register_pattern(
    "RED_DRAGON",
    display_name="Red Dragon",
    han=1,
    fu=0,
)
def red_dragon(self: PatternCalculator) -> int:
    """
    The hand contains a triplet or quad of the Centre.
    """
    return _yakuhai(self, 37)


@register_pattern(
    "YAKUHAI_PAIR",
    display_name="Yakuhai Pair",
    han=0,
    fu=2,
)
def yakuhaipair(self: PatternCalculator) -> int:
    """
    The hand's pair is the player seat's wind, wind round's wind,
    or a dragon (or the North wind if playing with 3 players).
    """
    if self.pair_count != 1:
        return 0
    yakuhai = [
        self.seat + 31,
        self.win.wind_round + 31,
        35,
        36,
        37,
    ]
    if self.win.player_count == 3:
        yakuhai.append(34)
    return sum(self.pair_tile == tile for tile in yakuhai)
