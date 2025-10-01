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


def remove_tile_value(tiles: list[TileId], tile_value: TileValue):
    for tile in tiles:
        if get_tile_value(tile) == tile_value:
            tiles.remove(tile)
            return tile
    raise Exception(f"Tile value {tile_value} not found in hand!")


def is_number(tile: TileValue):
    return tile < 30


def tile_id_is_flower(tile: TileId):
    return get_tile_value(tile) > 40


all_tiles = frozenset(
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    + [11, 12, 13, 14, 15, 16, 17, 18, 19]
    + [21, 22, 23, 24, 25, 26, 27, 28, 29]
    + [31, 32, 33, 34, 35, 36, 37]
)
orphans = {1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37}
terminals = {1, 9, 11, 19, 21, 29}
winds = {31, 32, 33, 34}
dragons = {35, 36, 37}
green_tiles = {22, 23, 24, 26, 28, 36}
