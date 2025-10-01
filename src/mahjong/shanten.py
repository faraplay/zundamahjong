from src.mahjong.tile import TileValue, all_tiles, orphans


def honours_shanten_data(tile_freqs: list[int]):
    # Expects values from 1 to 7 (need to subtract 30)
    data = [
        [0, 0b0000_000],
        [0, 0b0000_000],
        [0, 0b0000_000],
        [0, 0b0000_000],
        [0, 0b0000_000],
        [0, 0b0000_000],
        [0, 0b0000_000],
        [0, 0b0000_000],
        [0, 0b0000_000],
        [0, 0b0000_000],
    ]

    # remove triplets, keeping track of how many you remove
    triplet_count = 0
    current_tile = 0
    while current_tile < 7:
        if tile_freqs[current_tile] >= 3:
            triplet_count += 1
            tile_freqs[current_tile] -= 3
        else:
            current_tile += 1

    # get masks for the tiles with frequencies 1 and 2
    tile1_count = 0
    useful_tiles1 = 0b0000_000
    tile2_count = 0
    useful_tiles2 = 0b0000_000
    current_tile = 0
    while current_tile < 7:
        freq = tile_freqs[current_tile]
        if freq == 2:
            tile2_count += 1
            useful_tiles2 |= 0b1000_000 >> current_tile
        elif freq == 1:
            tile1_count += 1
            useful_tiles1 |= 0b1000_000 >> current_tile
        current_tile += 1

    meld_count = 0
    used_tile_count = 0
    useful_tiles = 0b0000_000
    # first we use complete triplets for our melds
    while meld_count < triplet_count:
        # there are still triplets left over so we can fill a pair
        data[meld_count * 2 + 1] = [used_tile_count + 2, useful_tiles]
        if meld_count >= 4:
            return data
        # use a triplet to fill a meld
        meld_count += 1
        used_tile_count += 3
        data[meld_count * 2] = [used_tile_count, useful_tiles]

    # next we use pairs for our melds
    while meld_count < triplet_count + tile2_count:
        # there are still pairs left over so we can fill a pair
        data[meld_count * 2 + 1] = [used_tile_count + 2, useful_tiles]
        if meld_count >= 4:
            return data
        # use a pair to fill a meld
        # now we have an incomplete meld so any tile with freq 2 is useful
        useful_tiles = useful_tiles2
        meld_count += 1
        used_tile_count += 2
        data[meld_count * 2] = [used_tile_count, useful_tiles]

    # next we use singles for our melds
    # we will have an incomplete meld using a single so any tile with
    # freq 1 or 2 is useful
    useful_tiles |= useful_tiles1
    while meld_count < triplet_count + tile2_count + tile1_count:
        data[meld_count * 2 + 1] = [used_tile_count + 1, useful_tiles]
        if meld_count >= 4:
            return data
        # use a single to fill a meld
        meld_count += 1
        used_tile_count += 1
        data[meld_count * 2] = [used_tile_count, useful_tiles]

    # we have no tiles left to fill melds
    # so any tile is useful
    useful_tiles = 0b1111_111
    while True:
        data[meld_count * 2 + 1] = [used_tile_count, useful_tiles]
        if meld_count >= 4:
            return data
        # add an empty meld
        meld_count += 1
        data[meld_count * 2] = [used_tile_count, useful_tiles]


def suit_shanten_data(tile_freqs: list[int]):
    # Given a list of tiles of a suit
    # return the number of tiles used in creating i melds and j pairs (0<=i<=4, 0<=j<=1)
    # and determine which tiles get you 1 closer
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

    def get_pair_useful_tiles(tile_freqs: list[int]):
        # Returns number of used tiles and bitflags of useful tiles for making a pair
        useful_tiles = 0b000_000_000
        current_tile = 0
        while current_tile < 9:
            freq = tile_freqs[current_tile]
            if freq >= 2:
                return 2, 0b000_000_000
            if freq == 1:
                useful_tiles |= 0b100_000_000 >> current_tile
            current_tile += 1
        if useful_tiles:
            return 1, useful_tiles
        else:
            return 0, 0b111_111_111

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
        pair_used_tile_count, pair_useful_tiles = get_pair_useful_tiles(unmelded_freqs)

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
        for current_tile in range(first_tile, 9):
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
                    useful_tiles | (0b100_000_000 >> current_tile),
                )
                freqs_copy[current_tile] += 1

            # see if we have any of the nextnext tile
            if current_tile + 2 < 9 and unmelded_freqs[current_tile + 2]:
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
                        useful_tiles | (0b010_000_000 >> current_tile),
                    )
                freqs_copy[current_tile + 2] += 1

            # see if we have any of the next tile
            if current_tile + 1 < 9 and unmelded_freqs[current_tile + 1]:
                freqs_copy[current_tile + 1] -= 1
                # try an incomplete meld with tile, tile + 1
                try_group(
                    freqs_copy,
                    current_tile,
                    meld_count + 1,
                    used_tile_count + 2,
                    useful_tiles | (0b1_001_000_000 >> current_tile),
                )
                freqs_copy[current_tile + 1] += 1

            # try a incomplete meld with just 1 tile
            try_group(
                freqs_copy,
                current_tile,
                meld_count + 1,
                used_tile_count + 1,
                useful_tiles | (0b11_111_000_000 >> current_tile),
            )

            freqs_copy[current_tile] += 1

    try_group(
        unmelded_freqs=tile_freqs,
        first_tile=0,
        meld_count=0,
        used_tile_count=0,
        useful_tiles=0b000_000_000,
    )
    for datum in data:
        datum[1] &= 0b111_111_111
    return data


def standard_shanten(tile_freqs: list[int], meld_count: int):
    def flag_to_tiles(flags: int, tile_end_offset: TileValue):
        result: list[TileValue] = []
        while flags != 0:
            if (flags % 2) != 0:
                result.append(tile_end_offset)
            tile_end_offset -= 1
            flags //= 2
        return frozenset(result)

    suit0_data = [
        (datum[0], flag_to_tiles(datum[1], 9))
        for datum in suit_shanten_data(tile_freqs[1:10])
    ]
    suit1_data = [
        (datum[0], flag_to_tiles(datum[1], 19))
        for datum in suit_shanten_data(tile_freqs[11:20])
    ]
    suit2_data = [
        (datum[0], flag_to_tiles(datum[1], 29))
        for datum in suit_shanten_data(tile_freqs[21:30])
    ]
    honours_data = [
        (datum[0], flag_to_tiles(datum[1], 37))
        for datum in honours_shanten_data(tile_freqs[31:38])
    ]

    def combine_data(
        data1: list[tuple[int, frozenset[TileValue]]],
        data2: list[tuple[int, frozenset[TileValue]]],
    ):
        data: list[tuple[int, frozenset[TileValue]]] = [(0, frozenset())] * 10
        for k1, datum1 in enumerate(data1):
            for k2, datum2 in enumerate(data2):
                if (k1 % 2) == 1 and (k2 % 2) == 1:
                    # both datums have a pair, skip
                    continue
                if k1 + k2 >= 10:
                    # too many melds, skip this and all larger values of k2
                    break
                used_tile_count = datum1[0] + datum2[0]
                useful_tiles_set = datum1[1] | datum2[1]
                existing_datum = data[k1 + k2]
                if used_tile_count > existing_datum[0]:
                    data[k1 + k2] = (used_tile_count, useful_tiles_set)
                elif used_tile_count == existing_datum[0]:
                    data[k1 + k2] = (
                        used_tile_count,
                        existing_datum[1] | useful_tiles_set,
                    )
        return data

    data = combine_data(
        combine_data(suit0_data, suit1_data), combine_data(suit2_data, honours_data)
    )
    return data[meld_count * 2 + 1]


def seven_pairs_shanten(tile_freqs: list[int]):
    tiles2 = set()
    tiles2_count = 0
    tiles1 = set()
    tiles1_count = 0
    for tile, freq in enumerate(tile_freqs):
        if freq >= 2:
            tiles2.add(tile)
            tiles2_count += 1
        elif freq == 1:
            tiles1.add(tile)
            tiles1_count += 1

    if tiles2_count >= 7:
        return (14, frozenset())

    if tiles2_count + tiles1_count >= 7:
        return (7 + tiles2_count, frozenset(tiles1))

    return (tiles2_count * 2 + tiles1_count, all_tiles - tiles2)


def thirteen_orphans_shanten(tile_freqs: list[int]):
    my_orphans = set()
    orphan_count = 0
    pair_orphan_count = 0
    for orphan in orphans:
        freq = tile_freqs[orphan]
        if freq >= 1:
            my_orphans.add(orphan)
            orphan_count += 1
        if freq >= 2:
            pair_orphan_count += 1
    if pair_orphan_count > 0:
        return (orphan_count + 1, orphans - my_orphans)
    else:
        return (orphan_count, orphans)


def calculate_shanten(tiles: list[TileValue]):
    assert len(tiles) % 3 == 1
    meld_count = (len(tiles) - 1) // 3

    tile_freqs = [0] * 38
    for tile in tiles:
        tile_freqs[tile] += 1

    def combine_datum(
        datum1: tuple[int, frozenset[TileValue]],
        datum2: tuple[int, frozenset[TileValue]],
    ):
        if datum1[0] > datum2[0]:
            return datum1
        elif datum1[0] < datum2[0]:
            return datum2
        else:
            return (datum1[0], datum1[1] | datum2[1])

    datum = standard_shanten(tile_freqs, meld_count)
    if len(tiles) == 13:
        datum = combine_datum(
            datum,
            combine_datum(
                seven_pairs_shanten(tile_freqs), thirteen_orphans_shanten(tile_freqs)
            ),
        )

    return (
        meld_count * 3 + 1 - datum[0],
        datum[1],
    )


def check_tenpai(tiles: list[TileValue]):
    shanten, waits = calculate_shanten(tiles)
    if shanten == 0:
        return waits
    else:
        return None
