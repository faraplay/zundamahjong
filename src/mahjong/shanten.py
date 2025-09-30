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

    def find_different_tile_index(
        tiles: list[TileValue], tile: TileValue, start_index: int
    ):
        "Returns the first index of a tile that is different, or -1 if not found"
        next_tile = 0
        index = start_index
        while index < len(tiles):
            next_tile = tiles[index]
            if next_tile != tile:
                return index
            index += 1
        return -1

    def popped(tiles: list[TileValue], index: int):
        tiles_copy = tiles.copy()
        tiles_copy.pop(index)
        return tiles_copy

    def popped2(tiles: list[TileValue], index: int):
        tiles_copy = tiles.copy()
        tiles_copy.pop(index)
        tiles_copy.pop(index)
        return tiles_copy

    def get_pair_useful_tiles(tiles: list[TileValue]):
        # Returns bitflags of the tiles that help make a pair
        # Assumes tiles is not empty!
        # Assumes tiles is sorted
        # Basically, if tiles contains a pair then it returns 0
        # Otherwise it returns bitflags of tiles
        length = len(tiles)
        current_index = 1
        useful_tiles = 0b1_000_000_000 >> tiles[0]
        while current_index < length:
            tile = tiles[current_index]
            if tile == tiles[current_index - 1]:
                return 0b000_000_000
            useful_tiles |= 0b1_000_000_000 >> tile
            current_index += 1
        return useful_tiles

    def try_group(
        unmelded_tiles: list[TileValue],
        first_index: int,
        meld_count: int,
        useful_tile_count: int,
        useful_tiles: int,
    ):
        # Tries to make melds, updates the data accordingly
        # Does not meld any tiles in tiles[:first_index]

        length = len(unmelded_tiles)

        # update data for current melds
        update_data(meld_count * 2, useful_tile_count, useful_tiles)

        # update data for current melds + a pair from leftover tiles
        if length > 0:
            pair_useful_tiles = get_pair_useful_tiles(unmelded_tiles)
            if pair_useful_tiles != 0:
                pair_useful_tile_count = useful_tile_count + 1
            else:
                pair_useful_tile_count = useful_tile_count + 2
            update_data(
                meld_count * 2 + 1,
                pair_useful_tile_count,
                useful_tiles | pair_useful_tiles,
            )
        if meld_count >= 4:
            # no point trying to make a 5th meld
            return

        if first_index >= length:
            # no tiles to check
            return

        if data[4 * 2 + 1][0] == 14:
            # we've already reached the best we can do, so stop
            return

        current_tile = unmelded_tiles[first_index]
        tiles_left1 = popped(unmelded_tiles, first_index)
        current_index = first_index
        while True:
            # see if we have two of current_tile
            if (
                current_index + 1 < length
                and tiles_left1[current_index] == current_tile
            ):
                # see if we have three of current_tile
                if (
                    current_index + 2 < length
                    and tiles_left1[current_index + 1] == current_tile
                ):
                    # no point trying two of the current tile if a third exists
                    # so we only try the meld of three
                    try_group(
                        popped2(tiles_left1, current_index),
                        current_index,
                        meld_count + 1,
                        useful_tile_count + 3,
                        useful_tiles,
                    )
                else:
                    try_group(
                        popped(tiles_left1, current_index),
                        current_index,
                        meld_count + 1,
                        useful_tile_count + 2,
                        useful_tiles | (0b1_000_000_000 >> current_tile),
                    )

            # find next different tile
            diff_index1 = find_different_tile_index(
                tiles_left1, current_tile, current_index
            )
            if diff_index1 != -1:
                diff_tile1 = tiles_left1[diff_index1]
                tiles_left2 = popped(tiles_left1, diff_index1)
                if diff_tile1 == current_tile + 1:
                    # find next next different tile
                    diff_index2 = find_different_tile_index(
                        tiles_left2, diff_tile1, diff_index1
                    )
                    if diff_index2 != -1:
                        diff_tile2 = tiles_left2[diff_index2]
                        if diff_tile2 == current_tile + 2:
                            # no point trying (tile, tile+2) when tile+1 exists
                            # just try using the meld tile, tile+1, tile+2
                            try_group(
                                popped(tiles_left2, diff_index2),
                                current_index,
                                meld_count + 1,
                                useful_tile_count + 3,
                                useful_tiles,
                            )
                    # try an incomplete meld with tile, tile + 1
                    try_group(
                        tiles_left2,
                        current_index,
                        meld_count + 1,
                        useful_tile_count + 2,
                        useful_tiles | (0b10_010_000_000 >> current_tile),
                    )
                elif diff_tile1 == current_tile + 2:
                    # try an incomplete meld with tile, tile + 2
                    try_group(
                        tiles_left2,
                        current_index,
                        meld_count + 1,
                        useful_tile_count + 2,
                        useful_tiles | (0b100_000_000 >> current_tile),
                    )

            # try a incomplete meld with just 1 tile
            try_group(
                tiles_left1,
                current_index,
                meld_count + 1,
                useful_tile_count + 1,
                useful_tiles | (0b111_110_000_000 >> current_tile),
            )

            if diff_index1 != -1:
                # move on to the next different tile
                # edit tiles_left1 in place
                tiles_left1[diff_index1] = current_tile
                current_tile = diff_tile1
                current_index = diff_index1 + 1
            else:
                return

    def update_data(data_index, useful_tile_count, useful_tiles):
        if useful_tile_count > data[data_index][0]:
            data[data_index][0] = useful_tile_count
            data[data_index][1] = useful_tiles
        elif useful_tile_count == data[data_index][0]:
            data[data_index][1] |= useful_tiles

    try_group(
        unmelded_tiles=sorted(tile_values),
        first_index=0,
        meld_count=0,
        useful_tile_count=0,
        useful_tiles=0b000_000_000,
    )
    for datum in data.values():
        datum[1] &= 0b111_111_111
    return data
