from ..tile import TileId, TileValue, get_tile_value, tile_id_is_flower
from .pattern_calculator import PatternCalculator, register_pattern


def get_dora_value(tile: TileId, is_3player: bool) -> TileValue:
    value = get_tile_value(tile)
    if is_3player and value == 1:
        return 9
    if value < 30 and value % 10 == 9:
        return value - 8
    if value == 34:
        return 31
    if value == 37:
        return 35
    return value + 1


def get_dora_flower_values(tile: TileId) -> list[TileValue]:
    value = get_tile_value(tile)
    if value <= 44:
        return [45, 46, 47, 48]
    else:
        return [41, 42, 43, 44]


def count_dora_matches(self: PatternCalculator, dora_tiles: list[TileId]) -> int:
    total = 0
    for dora_tile in dora_tiles:
        if tile_id_is_flower(dora_tile):
            total += sum(
                1
                for tile_value in self.flowers
                if tile_value in get_dora_flower_values(dora_tile)
            )
        else:
            total += sum(
                1
                for tile_value in self.hand_tiles
                if tile_value == get_dora_value(dora_tile, self.win.player_count == 3)
            )
    return total


@register_pattern(
    "DORA",
    display_name="Dora",
    dora=1,
)
def dora(self: PatternCalculator) -> int:
    """
    The number of (non-ura) dora tiles.
    """
    return count_dora_matches(self, self.win.dora)


@register_pattern(
    "URA_DORA",
    display_name="Ura Dora",
    dora=1,
)
def ura_dora(self: PatternCalculator) -> int:
    """
    The number of ura dora tiles.
    """
    if self.win.is_riichi:
        return count_dora_matches(self, self.win.ura_dora)
    else:
        return 0
