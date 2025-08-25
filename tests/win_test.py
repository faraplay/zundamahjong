import unittest

from src.mahjong.form_hand import is_winning, formed_hand_possibilities


class WinTest(unittest.TestCase):
    def test_wrong_size_hand(self):
        tiles = [1, 1, 1, 1]
        self.assertFalse(is_winning(tiles))

    def test_wrong_size_suits(self):
        tiles = [2, 2, 2, 2, 15, 15, 15, 15]
        self.assertFalse(is_winning(tiles))

    def test_number_pair(self):
        tiles = [5, 5]
        self.assertTrue(is_winning(tiles))

    def test_honor_pair(self):
        tiles = [31, 31]
        self.assertTrue(is_winning(tiles))

    def test_number_run(self):
        tiles = [1, 2, 3, 5, 5]
        self.assertTrue(is_winning(tiles))

    def test_number_run_unsorted(self):
        tiles = [2, 5, 3, 1, 5]
        self.assertTrue(is_winning(tiles))

    def test_number_bad_run(self):
        tiles = [1, 2, 2, 3, 4]
        self.assertFalse(is_winning(tiles))

    def test_number_triple_run(self):
        tiles = [1, 1, 1, 2, 2, 2, 3, 3, 3, 8, 8]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_number_double_run(self):
        tiles = [3, 3, 4, 4, 5, 5, 6, 6]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_honor_run(self):
        tiles = [2, 2, 31, 32, 33]
        self.assertFalse(is_winning(tiles))

    def test_number_overlapping_run(self):
        tiles = [2, 2, 3, 4, 4, 5, 5, 5, 6, 6, 7]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 1)

    def test_number_pon_run(self):
        tiles = [3, 3, 3, 4, 5, 6, 6, 6]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_many_suits_win(self):
        tiles = [4, 5, 6, 11, 11, 11, 26, 27, 27, 27, 28, 33, 33, 33]
        self.assertTrue(is_winning(tiles))

    def test_many_suits_not_win(self):
        tiles = [4, 5, 6, 11, 11, 11, 26, 26, 27, 27, 28, 33, 33, 33]
        self.assertFalse(is_winning(tiles))

    def test_nine_gates(self):
        tiles = [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9]
        for tile in range(1, 10):
            self.assertTrue(is_winning(tiles + [tile]))

    def test_seven_pairs(self):
        tiles = [1, 1, 5, 5, 9, 9, 13, 13, 15, 15, 27, 27, 35, 35]
        self.assertTrue(is_winning(tiles))

    def test_seven_pairs_repeat(self):
        tiles = [1, 1, 5, 5, 9, 9, 13, 13, 13, 13, 27, 27, 35, 35]
        self.assertFalse(is_winning(tiles))

    def test_four_pairs(self):
        tiles = [1, 1, 15, 15, 29, 29, 33, 33]
        self.assertFalse(is_winning(tiles))

    def test_ryanpeikou(self):
        tiles = [2, 2, 3, 3, 4, 4, 15, 15, 16, 16, 17, 17, 36, 36]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_thirteen_orphans(self):
        tiles = [1, 9, 11, 19, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37]
        self.assertTrue(is_winning(tiles))

    def test_eleven_orphans(self):
        tiles = [1, 9, 11, 19, 19, 21, 29, 31, 32, 33, 33, 33, 36, 37]
        self.assertFalse(is_winning(tiles))

    def test_thirteen_orphans_and_other(self):
        tiles = [1, 9, 11, 13, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37]
        self.assertFalse(is_winning(tiles))
