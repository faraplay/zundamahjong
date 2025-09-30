from src.mahjong.tile import TileValue

# Given a list of tiles of a suit
# return the number of extra tiles needed to create i melds and j pairs (0<=i<=4, 0<=j<=1)
# determine which tiles get you 1 closer


def suit_shanten_data(tile_values: list[TileValue]):
    data = [
        # i * 2 + j: (number of useful tiles, bitflags of which tiles get you closer)
        [0, 0b000_000_000],
        [0, 0b000_000_000],  # 1 pair
        [0, 0b000_000_000],  # 1 meld
        [0, 0b000_000_000],  # 1 meld 1 pair
        [0, 0b000_000_000],
        [0, 0b000_000_000],
        [0, 0b000_000_000],
        [0, 0b000_000_000],
        [0, 0b000_000_000],
        [0, 0b000_000_000],  # 4 melds 1 pair
    ]

    tile_freqs = [tile_values.count(tile) for tile in range(10)]

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

    def update_data(data_index, used_tile_count, useful_tiles):
        if used_tile_count > data[data_index][0]:
            data[data_index][0] = used_tile_count
            data[data_index][1] = useful_tiles
        elif used_tile_count == data[data_index][0]:
            data[data_index][1] |= useful_tiles

    def try_group(
        # unmelded_tiles: list[TileValue],
        unmelded_freqs: list[int],
        first_tile: TileValue,
        meld_count: int,
        used_tile_count: int,
        useful_tiles: int,
    ):
        # Tries to make melds, updates the data accordingly
        # Does not meld any tiles in tiles[:first_index]
        # (but it does use them for pairs)

        # determine if there are existing pairs in unmelded tiles
        pair_used_tile_count = min(max(unmelded_freqs), 2)
        if pair_used_tile_count == 0:
            pair_useful_tiles = 0b111_111_111
        elif pair_used_tile_count == 1:
            pair_useful_tiles = sum(
                0b1_000_000_000 >> tile
                for (tile, freq) in enumerate(unmelded_freqs)
                if freq
            )
        else:
            pair_useful_tiles = 0b000_000_000

        # update data for current melds
        update_data(meld_count * 2, used_tile_count, useful_tiles)
        update_data(
            meld_count * 2 + 1,
            used_tile_count + pair_used_tile_count,
            useful_tiles | pair_useful_tiles,
        )

        if meld_count >= 4:
            # no point trying to make a 5th meld
            return
        # update data for current melds + empty melds
        for meld_count_more in range(meld_count + 1, 5):
            update_data(meld_count_more * 2, used_tile_count, 0b111_111_111)
            update_data(
                meld_count_more * 2 + 1,
                used_tile_count + pair_used_tile_count,
                0b111_111_111,
            )

        if data[4 * 2 + 1][0] == 14:
            # we've already reached the best we can do, so stop
            return

        freqs_copy = unmelded_freqs.copy()
        for current_tile in range(first_tile, 10):
            # skip if we have none of current tile
            if unmelded_freqs[current_tile] == 0:
                continue

            freqs_copy[current_tile] -= 1

            # see if we have three of current_tile
            if unmelded_freqs[current_tile] >= 3:
                # no point trying two of the current tile if a third exists
                # so we only try the meld of three
                freqs_copy[current_tile] -= 2
                try_group(
                    freqs_copy,
                    current_tile,
                    meld_count + 1,
                    used_tile_count + 3,
                    useful_tiles,
                )
                freqs_copy[current_tile] += 2
            # see if we have two of current tile
            elif unmelded_freqs[current_tile] == 2:
                freqs_copy[current_tile] -= 1
                try_group(
                    freqs_copy,
                    current_tile,
                    meld_count + 1,
                    used_tile_count + 2,
                    useful_tiles | (0b1_000_000_000 >> current_tile),
                )
                freqs_copy[current_tile] += 1

            # see if we have any of the nextnext tile
            if current_tile + 2 < 10 and unmelded_freqs[current_tile + 2]:
                freqs_copy[current_tile + 2] -= 1
                # see if we have any of the next tile
                if unmelded_freqs[current_tile + 1]:
                    # no point trying (tile, tile+2) when tile+1 exists
                    # just try using the meld tile, tile+1, tile+2
                    freqs_copy[current_tile + 1] -= 1
                    try_group(
                        freqs_copy,
                        current_tile,
                        meld_count + 1,
                        used_tile_count + 3,
                        useful_tiles,
                    )
                    freqs_copy[current_tile + 1] += 1
                else:
                    # try an incomplete meld with tile, tile + 2
                    try_group(
                        freqs_copy,
                        current_tile,
                        meld_count + 1,
                        used_tile_count + 2,
                        useful_tiles | (0b100_000_000 >> current_tile),
                    )
                freqs_copy[current_tile + 2] += 1

            # see if we have any of the next tile
            if current_tile + 1 < 10 and unmelded_freqs[current_tile + 1]:
                freqs_copy[current_tile + 1] -= 1
                # try an incomplete meld with tile, tile + 1
                try_group(
                    freqs_copy,
                    current_tile,
                    meld_count + 1,
                    used_tile_count + 2,
                    useful_tiles | (0b10_010_000_000 >> current_tile),
                )
                freqs_copy[current_tile + 1] += 1

            # try a incomplete meld with just 1 tile
            try_group(
                freqs_copy,
                current_tile,
                meld_count + 1,
                used_tile_count + 1,
                useful_tiles | (0b111_110_000_000 >> current_tile),
            )

            freqs_copy[current_tile] += 1

    try_group(
        unmelded_freqs=tile_freqs,
        first_tile=1,
        meld_count=0,
        used_tile_count=0,
        useful_tiles=0b000_000_000,
    )
    for datum in data:
        datum[1] &= 0b111_111_111
    return data
