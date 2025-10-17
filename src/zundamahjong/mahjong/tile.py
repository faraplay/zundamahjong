TileId = int
TileValue = int

# Tiles are represented by integers
# Each tile in the deck has a unique integer
# To get the tile value, divide the tile by 4 (without remainder)
# 1-9 are 10ks
# 11-19 are biscuits
# 21-29 are sticks
# 31-37 are ESWNWhGR
# 41-48 are flowers

N = 10


def get_tile_value(tile: TileId) -> TileValue:
    return tile // N


def get_tile_values(tiles: list[TileId]) -> list[TileValue]:
    return [tile // N for tile in tiles]


def get_tile_value_buckets(tiles: list[TileId]) -> dict[int, list[int]]:
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
    for tile in tiles:
        if get_tile_value(tile) == tile_value:
            tiles.remove(tile)
            return tile
    raise Exception(f"Tile value {tile_value} not found in hand!")


def is_number(tile: TileValue) -> bool:
    return tile < 30


def tile_id_is_flower(tile: TileId) -> bool:
    return get_tile_value(tile) > 40


all_tiles = frozenset(
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    + [11, 12, 13, 14, 15, 16, 17, 18, 19]
    + [21, 22, 23, 24, 25, 26, 27, 28, 29]
    + [31, 32, 33, 34, 35, 36, 37]
)
tile_value_top = 38
orphans = frozenset({1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37})
terminals = frozenset({1, 9, 11, 19, 21, 29})
winds = frozenset({31, 32, 33, 34})
dragons = frozenset({35, 36, 37})
green_tiles = frozenset({22, 23, 24, 26, 28, 36})
