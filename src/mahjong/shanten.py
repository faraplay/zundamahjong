from collections import deque

from src.mahjong.tile import TileValue

# Given a list of tiles of a suit
# return the number of extra tiles needed to create i melds and j pairs (0<=i<=4, 0<=j<=1)
# determine which tiles get you 1 closer


def suit_shanten_data(tile_values: list[TileValue]):
    # Note we assume that we already have at least one tile for every meld we make
    # This looks stupid when we look at one suit but is valid when we combine all suits
    # (except for when the only helpful tiles are ones we already have 4 of)
    data = {
        # i * 2 + j: (number of useful tiles, bitflags of which tiles get you closer)
        0 * 2 + 0: [0, 0b000_000_000],
        0 * 2 + 1: [0, 0b000_000_000],  # 1 pair
        1 * 2 + 0: [0, 0b000_000_000],  # 1 meld
        1 * 2 + 1: [0, 0b000_000_000],  # 1 meld 1 pair
        2 * 2 + 0: [0, 0b000_000_000],
        2 * 2 + 1: [0, 0b000_000_000],
        3 * 2 + 0: [0, 0b000_000_000],
        3 * 2 + 1: [0, 0b000_000_000],
        4 * 2 + 0: [0, 0b000_000_000],
        4 * 2 + 1: [0, 0b000_000_000],  # 4 melds 1 pair
    }

    def find_different_tile(
        tiles: list[TileValue], current_index: int, tile: TileValue
    ):
        next_tile = 0
        index = current_index + 1
        while index < len(tiles):
            next_tile = tiles[index]
            if next_tile != tile:
                break
            index += 1
        return index, next_tile

    def try_group(
        tiles: list[TileValue],
        meld_count: int,
        pair_count: int,
        useful_tile_count: int,
        useful_tiles: int,
    ):
        if useful_tile_count > data[meld_count * 2 + pair_count][0]:
            data[meld_count * 2 + pair_count][0] = useful_tile_count
            data[meld_count * 2 + pair_count][1] = useful_tiles
        elif useful_tile_count == data[meld_count * 2 + pair_count][0]:
            data[meld_count * 2 + pair_count][1] |= useful_tiles
        for current_index in range(len(tiles)):
            tile = tiles[current_index]
            next_tile = (
                tiles[current_index + 1] if current_index + 1 < len(tiles) else 0
            )
            if pair_count < 1:
                # try a pair
                # no point trying an incomplete pair if there are two of that tile
                if next_tile == tile:
                    try_group(
                        tiles[current_index + 2 :],
                        meld_count,
                        pair_count + 1,
                        useful_tile_count + 2,
                        useful_tiles,
                    )
                else:
                    my_useful_tiles = 0b1_000_000_000 >> tile
                    try_group(
                        tiles[current_index + 1 :],
                        meld_count,
                        pair_count + 1,
                        useful_tile_count + 1,
                        useful_tiles | my_useful_tiles,
                    )
            if meld_count < 4:
                # try a incomplete meld with just 1 tile
                my_useful_tiles = 0b111_110_000_000 >> tile
                try_group(
                    tiles[current_index + 1 :],
                    meld_count + 1,
                    pair_count,
                    useful_tile_count + 1,
                    useful_tiles | my_useful_tiles,
                )
                # try an incomplete meld with more than one of the same tile
                if next_tile == tile:
                    # no point trying two tiles if the third exists
                    if (
                        current_index + 2 < len(tiles)
                        and tiles[current_index + 2] == tile
                    ):
                        try_group(
                            tiles[current_index + 3 :],
                            meld_count + 1,
                            pair_count,
                            useful_tile_count + 3,
                            useful_tiles,
                        )
                    else:
                        my_useful_tiles = 0b1_000_000_000 >> tile
                        try_group(
                            tiles[current_index + 2 :],
                            meld_count + 1,
                            pair_count,
                            useful_tile_count + 2,
                            useful_tiles | my_useful_tiles,
                        )
                # find next different tile
                different_index, next_different_tile = find_different_tile(
                    tiles, current_index, tile
                )
                remaining_tiles = tiles[current_index + 1 :]
                if next_different_tile == tile + 2:
                    # try an incomplete meld with tile, tile + 2
                    my_useful_tiles = 0b100_000_000 >> tile
                    remaining_tiles.remove(next_different_tile)
                    try_group(
                        remaining_tiles,
                        meld_count + 1,
                        pair_count,
                        useful_tile_count + 2,
                        useful_tiles | my_useful_tiles,
                    )
                elif next_different_tile == tile + 1:
                    # try an incomplete meld with tile, tile + 1
                    my_useful_tiles = 0b10_010_000_000 >> tile
                    remaining_tiles.remove(next_different_tile)
                    try_group(
                        remaining_tiles,
                        meld_count + 1,
                        pair_count,
                        useful_tile_count + 2,
                        useful_tiles | my_useful_tiles,
                    )
                    # find next next different tile
                    _, next_different_tile_2 = find_different_tile(
                        tiles, different_index, next_different_tile
                    )
                    if next_different_tile_2 == tile + 2:
                        # no point trying (tile, tile+2) when tile+1 exists
                        # just try using the meld tile, tile+1, tile+2
                        remaining_tiles.remove(next_different_tile_2)
                        try_group(
                            remaining_tiles,
                            meld_count + 1,
                            pair_count,
                            useful_tile_count + 3,
                            useful_tiles,
                        )

    try_group(sorted(tile_values), 0, 0, 0, 0b000_000_000)
    for datum in data.values():
        datum[1] &= 0b111_111_111
    return data
