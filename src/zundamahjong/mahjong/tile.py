TileId = int
"Represents a Mahjong tile. Every tile in the deck has a unique TileId."

TileValue = int
"""
Represents the value of a mahjong tile.

- 1-9 are manzu (characters)
- 11-19 are pinzu (dots)
- 21-29 are souzu (bamboos)
- 31-37 are jihai (winds and dragons, in the order ESWNWhGR)
- 41-48 are flowers (seasons and flowers)
"""

N = 10
"""
Constant used to calculate the value of a mahjong tile.

Mahjong tiles with tile id :math:`N a, N a + 1, ..., N a + (a - 1)`
all have tile value :math:`a`.
"""


def get_tile_value(tile: TileId) -> TileValue:
    "Return the value of a mahjong tile."
    return tile // N


def get_tile_values(tiles: list[TileId]) -> list[TileValue]:
    "Return a list of tile values given a list of tiles."
    return [tile // N for tile in tiles]


def get_tile_value_buckets(tiles: list[TileId]) -> dict[TileValue, list[TileId]]:
    "Sort tiles into buckets based on the tile's value."
    tile_value_buckets: dict[TileValue, list[TileId]] = {}
    for tile in tiles:
        tile_value = get_tile_value(tile)
        bucket = tile_value_buckets.get(tile_value)
        if bucket is None:
            bucket = []
            tile_value_buckets[tile_value] = bucket
        bucket.append(tile)
    return tile_value_buckets


def remove_tile_value(tiles: list[TileId], tile_value: TileValue) -> TileId:
    """
    Remove the first tile in the list with the specified value.

    Returns the removed tile.
    Raises an exception if no such tile is in the list.
    """
    for tile in tiles:
        if get_tile_value(tile) == tile_value:
            tiles.remove(tile)
            return tile
    raise Exception(f"Tile value {tile_value} not found in hand!")


def is_number(tile: TileValue) -> bool:
    """
    Return True if the tile value corresponds to a number tile.

    Return True if the tile value corresponds to a character tile,
    dot tile or bamboo tile.
    Return False if the tile value corresponds to
    an honour tile or flower tile.
    """
    return tile < 30


def tile_id_is_flower(tile: TileId) -> bool:
    """
    Return True if the tile is a flower tile.
    """
    return get_tile_value(tile) > 40


all_tiles = frozenset(
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    + [11, 12, 13, 14, 15, 16, 17, 18, 19]
    + [21, 22, 23, 24, 25, 26, 27, 28, 29]
    + [31, 32, 33, 34, 35, 36, 37]
)
"A frozenset containing all non-flower tile values."

tile_value_top = 38
"One more than the largest possible non-flower tile value."

orphans = frozenset({1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37})
"A frozenset containing the values of all orphan tiles."

terminals = frozenset({1, 9, 11, 19, 21, 29})
"A frozenset containing the values of all terminal tiles."

winds = frozenset({31, 32, 33, 34})
"A frozenset containing the values of all wind tiles."

dragons = frozenset({35, 36, 37})
"A frozenset containing the values of all dragon tiles."

green_tiles = frozenset({22, 23, 24, 26, 28, 36})
"A frozenset containing the values of all green tiles."
