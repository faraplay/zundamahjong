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
            return

        current_index = first_index
        while current_index < length:
            tile = unmelded_tiles[current_index]

            # try a incomplete meld with just 1 tile
            remaining_tiles = unmelded_tiles.copy()
            remaining_tiles.pop(current_index)
            my_useful_tiles = 0b111_110_000_000 >> tile
            try_group(
                remaining_tiles,
                current_index,
                meld_count + 1,
                useful_tile_count + 1,
                useful_tiles | my_useful_tiles,
            )
            if not current_index + 1 < length:
                # we've checked the last tile
                return

            # see if the tile immediately after the current tile is the same
            if remaining_tiles[current_index] == tile:
                # try an incomplete meld with more than one of the current tile
                remaining_tiles.pop(current_index)
                if (
                    current_index + 2 < length
                    and remaining_tiles[current_index] == tile
                ):
                    remaining_tiles.pop(current_index)
                    # no point trying two of the current tile if a third exists
                    try_group(
                        remaining_tiles,
                        current_index,
                        meld_count + 1,
                        useful_tile_count + 3,
                        useful_tiles,
                    )
                else:
                    my_useful_tiles = 0b1_000_000_000 >> tile
                    try_group(
                        remaining_tiles,
                        current_index,
                        meld_count + 1,
                        useful_tile_count + 2,
                        useful_tiles | my_useful_tiles,
                    )
                # remaining_tiles has been mangled, need to reconstruct it
                remaining_tiles = unmelded_tiles.copy()
                remaining_tiles.pop(current_index)

            # find next different tile
            different_index = find_different_tile_index(
                remaining_tiles, tile, current_index
            )
            if different_index == -1:
                # all later tiles are the same as this one
                return
            next_different_tile = remaining_tiles.pop(different_index)
            if next_different_tile == tile + 2:
                # try an incomplete meld with tile, tile + 2
                my_useful_tiles = 0b100_000_000 >> tile
                try_group(
                    remaining_tiles,
                    current_index,
                    meld_count + 1,
                    useful_tile_count + 2,
                    useful_tiles | my_useful_tiles,
                )
            elif next_different_tile == tile + 1:
                # try an incomplete meld with tile, tile + 1
                my_useful_tiles = 0b10_010_000_000 >> tile
                try_group(
                    remaining_tiles,
                    current_index,
                    meld_count + 1,
                    useful_tile_count + 2,
                    useful_tiles | my_useful_tiles,
                )
                # find next next different tile
                different_index_2 = find_different_tile_index(
                    remaining_tiles, next_different_tile, different_index
                )
                if different_index_2 != -1:
                    next_different_tile_2 = remaining_tiles.pop(different_index_2)
                    if next_different_tile_2 == tile + 2:
                        # no point trying (tile, tile+2) when tile+1 exists
                        # just try using the meld tile, tile+1, tile+2
                        try_group(
                            remaining_tiles,
                            current_index,
                            meld_count + 1,
                            useful_tile_count + 3,
                            useful_tiles,
                        )

            # move on to the next different tile
            # note that different_index was for the list remaining_tiles,
            # which had the current tile removed, so we need to add 1
            current_index = different_index + 1

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
