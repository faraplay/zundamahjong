type Datum = [number, Set<number>];

export function honours_shanten_data(tile_freqs: number[]) {
  const data: [number, number][] = [
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
  ];
  let triplet_count = 0;
  let current_tile = 0;
  while (current_tile < 7) {
    if (tile_freqs[current_tile] >= 3) {
      triplet_count += 1;
      tile_freqs[current_tile] -= 3;
    } else {
      current_tile += 1;
    }
  }
  let tile1_count = 0;
  let useful_tiles1 = 0b0000_000;
  let tile2_count = 0;
  let useful_tiles2 = 0b0000_000;
  for (current_tile = 0; current_tile < 7; current_tile += 1) {
    const freq = tile_freqs[current_tile];
    if (freq == 2) {
      tile2_count += 1;
      useful_tiles2 |= 0b1000_000 >> current_tile;
    } else if (freq == 1) {
      tile1_count += 1;
      useful_tiles1 |= 0b1000_000 >> current_tile;
    }
  }

  let meld_count = 0;
  let used_tile_count = 0;
  let useful_tiles = 0b0000_000;
  while (meld_count < triplet_count) {
    data[meld_count * 2 + 1] = [used_tile_count + 2, useful_tiles];
    if (meld_count >= 4) {
      return data;
    }
    meld_count += 1;
    used_tile_count += 3;
    data[meld_count * 2] = [used_tile_count, useful_tiles];
  }
  while (meld_count < triplet_count + tile2_count) {
    data[meld_count * 2 + 1] = [used_tile_count + 2, useful_tiles];
    if (meld_count >= 4) {
      return data;
    }
    useful_tiles = useful_tiles2;
    meld_count += 1;
    used_tile_count += 2;
    data[meld_count * 2] = [used_tile_count, useful_tiles];
  }
  useful_tiles |= useful_tiles1;
  while (meld_count < triplet_count + tile2_count + tile1_count) {
    data[meld_count * 2 + 1] = [used_tile_count + 1, useful_tiles];
    if (meld_count >= 4) {
      return data;
    }
    meld_count += 1;
    used_tile_count += 1;
    data[meld_count * 2] = [used_tile_count, useful_tiles];
  }
  useful_tiles = 0b1111_111;
  while (true) {
    data[meld_count * 2 + 1] = [used_tile_count, useful_tiles];
    if (meld_count >= 4) {
      return data;
    }
    meld_count += 1;
    data[meld_count * 2] = [used_tile_count, useful_tiles];
  }
}

export function suit_shanten_data(tile_freqs: number[]) {
  const data: [number, number][] = [
    [0, 0b000_000_000],
    [0, 0b000_000_000],
    [0, 0b000_000_000],
    [0, 0b000_000_000],
    [0, 0b000_000_000],
    [0, 0b000_000_000],
    [0, 0b000_000_000],
    [0, 0b000_000_000],
    [0, 0b000_000_000],
    [0, 0b000_000_000],
  ];

  function get_pair_useful_tiles(tile_freqs: number[]): [number, number] {
    let useful_tiles = 0b000_000_000;
    for (let current_tile = 0; current_tile < 9; current_tile += 1) {
      const freq = tile_freqs[current_tile];
      if (freq >= 2) {
        return [2, 0b000_000_000];
      }
      if (freq == 1) {
        useful_tiles |= 0b100_000_000 >> current_tile;
      }
    }
    if (useful_tiles) {
      return [1, useful_tiles];
    }
    return [0, 0b111_111_111];
  }

  function update_data(
    data_index: number,
    used_tile_count: number,
    useful_tiles: number,
  ) {
    if (used_tile_count > data[data_index][0]) {
      data[data_index][0] = used_tile_count;
      data[data_index][1] = useful_tiles;
    } else if (used_tile_count == data[data_index][0]) {
      data[data_index][1] |= useful_tiles;
    }
  }

  function try_group(
    unmelded_freqs: number[],
    first_tile: number,
    meld_count: number,
    used_tile_count: number,
    useful_tiles: number,
  ) {
    const [pair_used_tile_count, pair_useful_tiles] =
      get_pair_useful_tiles(unmelded_freqs);
    update_data(meld_count * 2, used_tile_count, useful_tiles);
    update_data(
      meld_count * 2 + 1,
      used_tile_count + pair_used_tile_count,
      useful_tiles | pair_useful_tiles,
    );

    if (meld_count >= 4) {
      return;
    }
    for (
      let meld_count_more = meld_count + 1;
      meld_count_more < 5;
      meld_count_more += 1
    ) {
      update_data(meld_count_more * 2, used_tile_count, 0b111_111_111);
      update_data(
        meld_count_more * 2 + 1,
        used_tile_count + pair_used_tile_count,
        0b111_111_111,
      );
    }

    if (data[4 * 2 + 1][0] == 14) {
      return;
    }

    const freqs_copy = [...unmelded_freqs];
    for (let current_tile = first_tile; current_tile < 9; current_tile += 1) {
      if (unmelded_freqs[current_tile] == 0) {
        continue;
      }

      freqs_copy[current_tile] -= 1;
      if (unmelded_freqs[current_tile] >= 3) {
        freqs_copy[current_tile] -= 2;
        try_group(
          freqs_copy,
          current_tile,
          meld_count + 1,
          used_tile_count + 3,
          useful_tiles,
        );
        freqs_copy[current_tile] += 2;
      } else if (unmelded_freqs[current_tile] == 2) {
        freqs_copy[current_tile] -= 1;
        try_group(
          freqs_copy,
          current_tile,
          meld_count + 1,
          used_tile_count + 2,
          useful_tiles | (0b100_000_000 >> current_tile),
        );
        freqs_copy[current_tile] += 1;
      }
      if (current_tile + 2 < 9 && unmelded_freqs[current_tile + 2]) {
        freqs_copy[current_tile + 2] -= 1;
        if (unmelded_freqs[current_tile + 1]) {
          freqs_copy[current_tile + 1] -= 1;
          try_group(
            freqs_copy,
            current_tile,
            meld_count + 1,
            used_tile_count + 3,
            useful_tiles,
          );
          freqs_copy[current_tile + 1] += 1;
        } else {
          try_group(
            freqs_copy,
            current_tile,
            meld_count + 1,
            used_tile_count + 2,
            useful_tiles | (0b010_000_000 >> current_tile),
          );
        }
        freqs_copy[current_tile + 2] += 1;
      }
      if (current_tile + 1 < 9 && unmelded_freqs[current_tile + 1]) {
        freqs_copy[current_tile + 1] -= 1;
        try_group(
          freqs_copy,
          current_tile,
          meld_count + 1,
          used_tile_count + 2,
          useful_tiles | (0b1_001_000_000 >> current_tile),
        );
        freqs_copy[current_tile + 1] += 1;
      }
      try_group(
        freqs_copy,
        current_tile,
        meld_count + 1,
        used_tile_count + 1,
        useful_tiles | (0b11_111_000_000 >> current_tile),
      );

      freqs_copy[current_tile] += 1;
    }
  }

  try_group(tile_freqs, 0, 0, 0, 0b000_000_000);
  for (const datum of data) {
    datum[1] &= 0b111_111_111;
  }
  return data;
}

function standard_shanten(tile_freqs: number[], meld_count: number) {
  function flag_to_tiles(flags: number, tile_end_offset: number) {
    const result: number[] = [];
    while (flags != 0) {
      if (flags % 2 != 0) {
        result.push(tile_end_offset);
      }
      tile_end_offset -= 1;
      flags = Math.trunc(flags / 2);
    }
    return new Set(result);
  }

  const suit0_data: Datum[] = suit_shanten_data(tile_freqs.slice(1, 10)).map(
    (datum) => [datum[0], flag_to_tiles(datum[1], 9)],
  );
  const suit1_data: Datum[] = suit_shanten_data(tile_freqs.slice(11, 20)).map(
    (datum) => [datum[0], flag_to_tiles(datum[1], 19)],
  );
  const suit2_data: Datum[] = suit_shanten_data(tile_freqs.slice(21, 30)).map(
    (datum) => [datum[0], flag_to_tiles(datum[1], 29)],
  );
  const honours_data: Datum[] = honours_shanten_data(
    tile_freqs.slice(31, 38),
  ).map((datum) => [datum[0], flag_to_tiles(datum[1], 37)]);

  function combine_data(data1: Datum[], data2: Datum[]): Datum[] {
    const data: Datum[] = [
      [0, new Set()],
      [0, new Set()],
      [0, new Set()],
      [0, new Set()],
      [0, new Set()],
      [0, new Set()],
      [0, new Set()],
      [0, new Set()],
      [0, new Set()],
      [0, new Set()],
    ];
    for (const [k1, datum1] of data1.entries()) {
      for (const [k2, datum2] of data2.entries()) {
        if (k1 % 2 == 1 && k2 % 2 == 1) {
          continue;
        }
        if (k1 + k2 >= 10) {
          break;
        }
        const used_tile_count = datum1[0] + datum2[0];
        const useful_tiles_set = new Set([...datum1[1], ...datum2[1]]);
        const existing_datum = data[k1 + k2];
        if (used_tile_count > existing_datum[0]) {
          data[k1 + k2] = [used_tile_count, useful_tiles_set];
        } else if (used_tile_count == existing_datum[0]) {
          data[k1 + k2] = [
            used_tile_count,
            new Set([...existing_datum[1], ...useful_tiles_set]),
          ];
        }
      }
    }
    return data;
  }

  const data = combine_data(
    combine_data(suit0_data, suit1_data),
    combine_data(suit2_data, honours_data),
  );
  return data[meld_count * 2 + 1];
}

const all_tiles = [
  1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24,
  25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37,
];

function seven_pairs_shanten(tile_freqs: number[]): Datum {
  const tiles2 = new Set<number>();
  let tiles2_count = 0;
  const tiles1 = new Set<number>();
  let tiles1_count = 0;
  for (const [tile, freq] of tile_freqs.entries()) {
    if (freq >= 2) {
      tiles2.add(tile);
      tiles2_count += 1;
    } else if (freq == 1) {
      tiles1.add(tile);
      tiles1_count += 1;
    }
  }

  if (tiles2_count >= 7) {
    return [14, new Set()];
  }

  if (tiles2_count + tiles1_count >= 7) {
    return [7 + tiles2_count, new Set(tiles1)];
  }

  return [
    tiles2_count * 2 + tiles1_count,
    new Set(all_tiles.filter((tile) => !tiles2.has(tile))),
  ];
}

const orphans = [1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37];

function thirteen_orphans_shanten(tile_freqs: number[]): Datum {
  const my_orphans = new Set<number>();
  let orphan_count = 0;
  let pair_orphan_count = 0;
  for (const orphan of orphans) {
    const freq = tile_freqs[orphan];
    if (freq >= 1) {
      my_orphans.add(orphan);
      orphan_count += 1;
    }
    if (freq >= 2) {
      pair_orphan_count += 1;
    }
  }
  if (pair_orphan_count > 0) {
    return [
      orphan_count + 1,
      new Set(orphans.filter((tile) => !my_orphans.has(tile))),
    ];
  }
  return [orphan_count, new Set(orphans)];
}

export function calculate_shanten(tiles: number[]): Datum {
  const meld_count = Math.trunc((tiles.length - 1) / 3);

  const tile_freqs = Array<number>(38).fill(0);
  for (const tile of tiles) {
    if (tile < 38) {
      tile_freqs[tile] += 1;
    }
  }

  function combine_datum(datum1: Datum, datum2: Datum): Datum {
    if (datum1[0] > datum2[0]) {
      return datum1;
    } else if (datum1[0] < datum2[0]) {
      return datum2;
    }
    return [datum1[0], new Set([...datum1[1], ...datum2[1]])];
  }

  let datum: Datum = standard_shanten(tile_freqs, meld_count);
  if (tiles.length == 13) {
    datum = combine_datum(
      datum,
      combine_datum(
        seven_pairs_shanten(tile_freqs),
        thirteen_orphans_shanten(tile_freqs),
      ),
    );
  }

  return [meld_count * 3 + 1 - datum[0], datum[1]];
}

export function check_tenpai(tiles: number[]): Set<number> {
  if (tiles.length % 3 != 1) {
    return new Set();
  }
  if (tiles.some((tile) => tile >= 38)) {
    return new Set();
  }
  const [shanten, waits] = calculate_shanten(tiles);
  if (shanten == 0) {
    return waits;
  }
  return new Set();
}
