Tile = int

# Tiles are represented by integers
# 1-9 are 10ks
# 11-19 are biscuits
# 21-29 are sticks
# 31-37 are ESWNWhGR
# 41-48 are flowers


def is_number(tile: Tile):
    return tile < 30


def is_flower(tile: Tile):
    return tile > 40
