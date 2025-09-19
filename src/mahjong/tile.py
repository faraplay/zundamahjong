Tile = int

# Tiles are represented by integers
# 1-9 are 10ks
# 11-19 are biscuits
# 21-29 are sticks
# 31-37 are ESWNWhGR
# 41-48 are flowers


def is_number(tile: Tile):
    return tile // 4 < 30


def is_honour(tile: Tile):
    return 30 < tile // 4 < 40


def is_flower(tile: Tile):
    return tile // 4 > 40


orphans = {1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37}
terminals = {1, 9, 11, 19, 21, 29}
winds = {31, 32, 33, 34}
dragons = {35, 36, 37}
green_tiles = {22, 23, 24, 26, 28, 36}


def is_orphan(tile: Tile):
    return tile // 4 in orphans
