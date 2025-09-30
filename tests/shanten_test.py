import unittest

from src.mahjong.shanten import suit_shanten_data


class ShantenTest(unittest.TestCase):
    def test_shanten_1(self):
        data = suit_shanten_data([1])
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

    def test_shanten_5(self):
        data = suit_shanten_data([5])
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

    def test_shanten_34(self):
        data = suit_shanten_data([3, 4])
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

    def test_shanten_2344(self):
        data = suit_shanten_data([2, 3, 4, 4])
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

    def test_shanten_233444556(self):
        data = suit_shanten_data([2, 3, 3, 4, 4, 4, 5, 5, 6])
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

    def test_shanten_times_1000(self):
        for _ in range(1000):
            suit_shanten_data([2, 3, 3, 4, 4, 4, 5, 5, 6])

    def test_shanten_long_times_1000(self):
        for _ in range(1000):
            suit_shanten_data([2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 9, 9, 9])

    def test_shanten_all(self):
        def hand_from_code(hand_code):
            hand = []
            for tile in range(1, 10):
                for _ in range(hand_code % 5):
                    hand.append(tile)
                hand_code //= 5
            return hand

        def code_from_hand(hand):
            return sum(5 ** (i - 1) for i in hand)

        limit = 5**6
        datas = []
        for hand_code in range(limit):
            hand = hand_from_code(hand_code)
            assert hand_code == code_from_hand(hand)
            datas.append(suit_shanten_data(hand))

        for hand_code, data in enumerate(datas):
            for tile in range(1, 10):
                if hand_from_code(hand_code).count(tile) == 4:
                    continue
                mask = 0b1_000_000_000 >> tile
                added_hand_code = hand_code + (5 ** (tile - 1))
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
