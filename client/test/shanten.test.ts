import { expect, test } from "vitest";
import {
  calculate_shanten,
  honours_shanten_data,
  suit_shanten_data,
} from "../src/shanten";

test("Test honours_shanten_1", () => {
  expect(honours_shanten_data([1, 0, 0, 0, 0, 0, 0])).toEqual([
    [0, 0b0000_000],
    [1, 0b1000_000],
    [1, 0b1000_000],
    [1, 0b1111_111],
    [1, 0b1111_111],
    [1, 0b1111_111],
    [1, 0b1111_111],
    [1, 0b1111_111],
    [1, 0b1111_111],
    [1, 0b1111_111],
  ]);
});

test("Test honours_shanten_112", () => {
  expect(honours_shanten_data([2, 1, 0, 0, 0, 0, 0])).toEqual([
    [0, 0b0000_000],
    [2, 0b0000_000],
    [2, 0b1000_000],
    [3, 0b1100_000],
    [3, 0b1100_000],
    [3, 0b1111_111],
    [3, 0b1111_111],
    [3, 0b1111_111],
    [3, 0b1111_111],
    [3, 0b1111_111],
  ]);
});

test("Test honours_shanten_11123", () => {
  expect(honours_shanten_data([3, 1, 1, 0, 0, 0, 0])).toEqual([
    [0, 0b0000_000],
    [2, 0b0000_000],
    [3, 0b0000_000],
    [4, 0b0110_000],
    [4, 0b0110_000],
    [5, 0b0110_000],
    [5, 0b0110_000],
    [5, 0b1111_111],
    [5, 0b1111_111],
    [5, 0b1111_111],
  ]);
});

test("Test honours_shanten_112234", () => {
  expect(honours_shanten_data([2, 2, 1, 1, 0, 0, 0])).toEqual([
    [0, 0b0000_000],
    [2, 0b0000_000],
    [2, 0b1100_000],
    [4, 0b1100_000],
    [4, 0b1100_000],
    [5, 0b1111_000],
    [5, 0b1111_000],
    [6, 0b1111_000],
    [6, 0b1111_000],
    [6, 0b1111_111],
  ]);
});

test("Test honours_shanten_11112234", () => {
  expect(honours_shanten_data([4, 2, 1, 1, 0, 0, 0])).toEqual([
    [0, 0b0000_000],
    [2, 0b0000_000],
    [3, 0b0000_000],
    [5, 0b0000_000],
    [5, 0b0100_000],
    [6, 0b1111_000],
    [6, 0b1111_000],
    [7, 0b1111_000],
    [7, 0b1111_000],
    [8, 0b1111_000],
  ]);
});

test("Test suit_shanten_1", () => {
  expect(suit_shanten_data([1, 0, 0, 0, 0, 0, 0, 0, 0])).toEqual([
    [0, 0b000_000_000],
    [1, 0b100_000_000],
    [1, 0b111_000_000],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
  ]);
});

test("Test suit_shanten_5", () => {
  expect(suit_shanten_data([0, 0, 0, 0, 1, 0, 0, 0, 0])).toEqual([
    [0, 0b000_000_000],
    [1, 0b000_010_000],
    [1, 0b001_111_100],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
    [1, 0b111_111_111],
  ]);
});

test("Test suit_shanten_34", () => {
  expect(suit_shanten_data([0, 0, 1, 1, 0, 0, 0, 0, 0])).toEqual([
    [0, 0b000_000_000],
    [1, 0b001_100_000],
    [2, 0b010_010_000],
    [2, 0b111_111_111],
    [2, 0b111_111_111],
    [2, 0b111_111_111],
    [2, 0b111_111_111],
    [2, 0b111_111_111],
    [2, 0b111_111_111],
    [2, 0b111_111_111],
  ]);
});

test("Test suit_shanten_2344", () => {
  expect(suit_shanten_data([0, 1, 1, 2, 0, 0, 0, 0, 0])).toEqual([
    [0, 0b000_000_000],
    [2, 0b000_000_000],
    [3, 0b000_000_000],
    [4, 0b100_100_000],
    [4, 0b111_111_000],
    [4, 0b111_111_111],
    [4, 0b111_111_111],
    [4, 0b111_111_111],
    [4, 0b111_111_111],
    [4, 0b111_111_111],
  ]);
});

test("Test suit_shanten_233444556", () => {
  expect(suit_shanten_data([0, 1, 2, 3, 2, 1, 0, 0, 0])).toEqual([
    [0, 0b000_000_000],
    [2, 0b000_000_000],
    [3, 0b000_000_000],
    [5, 0b000_000_000],
    [6, 0b000_000_000],
    [7, 0b111_111_100],
    [9, 0b000_000_000],
    [9, 0b111_111_111],
    [9, 0b111_111_111],
    [9, 0b111_111_111],
  ]);
});

test("Test suit_shanten_times_1000", () => {
  for (let i = 0; i++; i < 1000) {
    suit_shanten_data([0, 1, 2, 3, 2, 1, 0, 0, 0]);
  }
});

test("Test suit_shanten_long_times_1000", () => {
  for (let i = 0; i++; i < 1000) {
    suit_shanten_data([0, 1, 2, 3, 2, 4, 3, 1, 3]);
  }
});

test("Test suit_shanten_all", () => {
  function hand_from_code(hand_code: number) {
    const hand = [];
    for (let i = 0; i < 9; i++) {
      hand.push(hand_code % 5);
      hand_code = Math.trunc(hand_code / 5);
    }
    return hand;
  }

  const limit = 5 * 5 * 5 * 5 * 5 * 5;
  const datas = [];
  for (let hand_code = 0; hand_code < limit; hand_code++) {
    const hand = hand_from_code(hand_code);
    datas.push(suit_shanten_data(hand));
  }

  for (const [hand_code, data] of datas.entries()) {
    for (let tile = 0; tile < 9; tile++) {
      if (hand_from_code(hand_code)[tile] == 4) {
        continue;
      }
      const mask = 0b100_000_000 >> tile;
      const added_hand_code = hand_code + 5 ** tile;
      if (added_hand_code >= limit) {
        break;
      }
      for (let k = 0; k < 10; k++) {
        if (data[k][1] & mask) {
          expect(data[k][0] + 1).toEqual(datas[added_hand_code][k][0]);
        } else {
          expect(data[k][0]).toEqual(datas[added_hand_code][k][0]);
        }
      }
    }
  }
}, 60_000);

test("Test shanten_1shanten_small", () => {
  const [shanten, useful_tiles] = calculate_shanten([2, 3, 15, 32], false);
  expect(shanten).toEqual(1);
  expect(useful_tiles).toEqual(new Set([1, 4, 15, 32]));
});

test("Test shanten_1shanten", () => {
  const [shanten, useful_tiles] = calculate_shanten(
    [5, 6, 7, 8, 9, 17, 18, 19, 23, 24, 29, 29, 29],
    false,
  );
  expect(shanten).toEqual(1);
  expect(useful_tiles).toEqual(new Set([4, 5, 6, 7, 8, 9, 22, 23, 24, 25]));
});

test("Test shanten_2shanten", () => {
  const [shanten, useful_tiles] = calculate_shanten(
    [7, 8, 12, 14, 18, 18, 23, 24, 24, 26, 27, 27, 28],
    false,
  );
  expect(shanten).toEqual(2);
  expect(useful_tiles).toEqual(new Set([6, 9, 13, 18, 22, 24, 25]));
});

test("Test shanten_2shanten_allow7pairs", () => {
  const [shanten, useful_tiles] = calculate_shanten(
    [3, 4, 4, 11, 12, 13, 17, 17, 24, 26, 26, 35, 35],
    false,
  );
  expect(shanten).toEqual(2);
  expect(useful_tiles).toEqual(
    new Set([2, 3, 4, 5, 11, 12, 13, 17, 24, 25, 26, 35]),
  );
});

test("Test shanten_3shanten", () => {
  const [shanten, useful_tiles] = calculate_shanten(
    [14, 17, 18, 22, 24, 25, 26, 27, 28, 33, 35, 37, 37],
    false,
  );
  expect(shanten).toEqual(3);
  expect(useful_tiles).toEqual(
    new Set([
      12, 13, 14, 15, 16, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33, 35, 37,
    ]),
  );
});

test("Test shanten_4shanten_allow7pairs_allow13orphans", () => {
  const [shanten, useful_tiles] = calculate_shanten(
    [1, 9, 11, 19, 21, 23, 31, 31, 31, 31, 32, 32, 33],
    false,
  );
  expect(shanten).toEqual(4);
  expect(useful_tiles).toEqual(
    new Set([
      1, 2, 3, 7, 8, 9, 11, 12, 13, 17, 18, 19, 21, 22, 23, 29, 31, 32, 33, 34,
      35, 36, 37,
    ]),
  );
});

test("Test shanten_3player", () => {
  const [shanten, useful_tiles] = calculate_shanten([1, 9, 25, 25], true);
  expect(shanten).toEqual(1);
  expect(useful_tiles).toEqual(new Set([1, 9, 25]));
});
