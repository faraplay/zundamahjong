import unittest

from zundamahjong.mahjong.shanten import (
    honours_shanten_data,
    suit_shanten_data,
    calculate_shanten,
)


class ShantenTest(unittest.TestCase):
    def test_honours_shanten_1(self) -> None:
        data = honours_shanten_data([1, 0, 0, 0, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_honours_shanten_112(self) -> None:
        data = honours_shanten_data([2, 1, 0, 0, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_honours_shanten_11123(self) -> None:
        data = honours_shanten_data([3, 1, 1, 0, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_honours_shanten_112234(self) -> None:
        data = honours_shanten_data([2, 2, 1, 1, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_honours_shanten_11112234(self) -> None:
        data = honours_shanten_data([4, 2, 1, 1, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_suit_shanten_1(self) -> None:
        data = suit_shanten_data([1, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_suit_shanten_5(self) -> None:
        data = suit_shanten_data([0, 0, 0, 0, 1, 0, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_suit_shanten_34(self) -> None:
        data = suit_shanten_data([0, 0, 1, 1, 0, 0, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_suit_shanten_2344(self) -> None:
        data = suit_shanten_data([0, 1, 1, 2, 0, 0, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_suit_shanten_233444556(self) -> None:
        data = suit_shanten_data([0, 1, 2, 3, 2, 1, 0, 0, 0])
        self.assertEqual(
            data,
            [
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
            ],
        )

    def test_suit_shanten_times_1000(self) -> None:
        for _ in range(1000):
            suit_shanten_data([0, 1, 2, 3, 2, 1, 0, 0, 0])

    def test_suit_shanten_long_times_1000(self) -> None:
        for _ in range(1000):
            suit_shanten_data([0, 1, 2, 3, 2, 4, 3, 1, 3])

    def test_suit_shanten_all(self) -> None:
        def hand_from_code(hand_code: int) -> list[int]:
            hand: list[int] = []
            for _ in range(9):
                hand.append(hand_code % 5)
                hand_code //= 5
            return hand

        def code_from_hand(hand: list[int]) -> int:
            return sum(count * 5**tile for tile, count in enumerate(hand))

        limit = 5**6
        datas: list[list[list[int]]] = []
        for hand_code in range(limit):
            hand = hand_from_code(hand_code)
            assert hand_code == code_from_hand(hand)
            datas.append(suit_shanten_data(hand))

        for hand_code, data in enumerate(datas):
            for tile in range(9):
                if hand_from_code(hand_code)[tile] == 4:
                    continue
                mask = 0b100_000_000 >> tile
                added_hand_code = hand_code + 5**tile  # pyright: ignore[reportAny]
                if added_hand_code >= limit:
                    break
                for k in range(10):
                    if data[k][1] & mask:
                        self.assertEqual(
                            data[k][0] + 1,
                            datas[added_hand_code][k][0],
                            f"hand is {hand_from_code(hand_code)}, tile is {tile}, k is {k}",
                        )
                    else:
                        self.assertEqual(
                            data[k][0],
                            datas[added_hand_code][k][0],
                            f"hand is {hand_from_code(hand_code)}, tile is {tile}, k is {k}",
                        )

    def test_shanten_1shanten_small(self) -> None:
        shanten, useful_tiles = calculate_shanten([2, 3, 15, 32])
        self.assertEqual(shanten, 1)
        self.assertSetEqual(useful_tiles, {1, 4, 15, 32})

    def test_shanten_1shanten(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [5, 6, 7, 8, 9, 17, 18, 19, 23, 24, 29, 29, 29]
        )
        self.assertEqual(shanten, 1)
        self.assertSetEqual(useful_tiles, {4, 5, 6, 7, 8, 9, 22, 23, 24, 25})

    def test_shanten_2shanten(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [7, 8, 12, 14, 18, 18, 23, 24, 24, 26, 27, 27, 28]
        )
        self.assertEqual(shanten, 2)
        self.assertSetEqual(useful_tiles, {6, 9, 13, 18, 22, 24, 25})

    def test_shanten_2shanten_allow7pairs(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [3, 4, 4, 11, 12, 13, 17, 17, 24, 26, 26, 35, 35]
        )
        self.assertEqual(shanten, 2)
        self.assertSetEqual(useful_tiles, {2, 3, 4, 5, 11, 12, 13, 17, 24, 25, 26, 35})

    def test_shanten_3shanten(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [14, 17, 18, 22, 24, 25, 26, 27, 28, 33, 35, 37, 37]
        )
        self.assertEqual(shanten, 3)
        self.assertSetEqual(
            useful_tiles,
            {12, 13, 14, 15, 16, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33, 35, 37},
        )

    def test_shanten_4shanten_allow7pairs_allow13orphans(self) -> None:
        shanten, useful_tiles = calculate_shanten(
            [1, 9, 11, 19, 21, 23, 31, 31, 31, 31, 32, 32, 33]
        )
        self.assertEqual(shanten, 4)
        self.assertSetEqual(
            useful_tiles,
            {
                1,
                2,
                3,
                7,
                8,
                9,
                11,
                12,
                13,
                17,
                18,
                19,
                21,
                22,
                23,
                29,
                31,
                32,
                33,
                34,
                35,
                36,
                37,
            },
        )

    def test_shanten_3player(self) -> None:
        shanten, useful_tiles = calculate_shanten([1, 9, 25, 25], is_3player=True)
        self.assertEqual(shanten, 1)
        self.assertSetEqual(
            useful_tiles,
            {1, 9, 25},
        )
