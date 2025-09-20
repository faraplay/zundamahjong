Tile = int
TileValue = int

# Tiles are represented by integers
# Each tile in the deck has a unique integer
# To get the tile value, divide the tile by 4 (without remainder)
# 1-9 are 10ks
# 11-19 are biscuits
# 21-29 are sticks
# 31-37 are ESWNWhGR
# 41-48 are flowers


def get_tile_values(tiles: list[Tile]) -> list[TileValue]:
    return [tile // 4 for tile in tiles]


def remove_tile_value(tiles: list[Tile], tile_value: TileValue):
    for tile in tiles:
        if tile // 4 == tile_value:
            tiles.remove(tile)
            return tile
    raise Exception(f"Tile value {tile_value} not found in hand!")


def is_number(tile: Tile):
    return tile < 30


def tile_is_flower(tile: Tile):
    return tile // 4 > 40


orphans = {1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37}
terminals = {1, 9, 11, 19, 21, 29}
winds = {31, 32, 33, 34}
dragons = {35, 36, 37}
green_tiles = {22, 23, 24, 26, 28, 36}


def is_orphan(tile: Tile):
    return tile // 4 in orphans
