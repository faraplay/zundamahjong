import unittest

from src.mahjong.form_hand import is_winning, formed_hand_possibilities


class FormHandTest(unittest.TestCase):
    def test_wrong_size_hand(self):
        tiles = [4, 5, 6, 7]
        self.assertFalse(is_winning(tiles))

    def test_wrong_size_suits(self):
        tiles = [8, 9, 10, 11, 60, 61, 62, 63]
        self.assertFalse(is_winning(tiles))

    def test_number_pair(self):
        tiles = [20, 21]
        self.assertTrue(is_winning(tiles))

    def test_honor_pair(self):
        tiles = [124, 125]
        self.assertTrue(is_winning(tiles))

    def test_number_run(self):
        tiles = [4, 8, 12, 20, 21]
        self.assertTrue(is_winning(tiles))

    def test_number_run_unsorted(self):
        tiles = [8, 20, 12, 4, 21]
        self.assertTrue(is_winning(tiles))

    def test_number_bad_run(self):
        tiles = [4, 8, 9, 12, 16]
        self.assertFalse(is_winning(tiles))

    def test_number_triple_run(self):
        tiles = [4, 5, 6, 8, 9, 10, 12, 13, 14, 32, 33]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_number_double_run(self):
        tiles = [12, 13, 16, 17, 20, 21, 24, 25]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_honor_run(self):
        tiles = [8, 9, 124, 128, 132]
        self.assertFalse(is_winning(tiles))

    def test_number_overlapping_run(self):
        tiles = [8, 9, 12, 16, 17, 20, 21, 22, 24, 25, 28]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 1)

    def test_number_pon_run(self):
        tiles = [12, 13, 14, 16, 20, 24, 25, 26]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_many_suits_win(self):
        tiles = [16, 20, 24, 44, 45, 46, 104, 108, 109, 110, 112, 132, 133, 134]
        self.assertTrue(is_winning(tiles))

    def test_many_suits_not_win(self):
        tiles = [16, 20, 24, 44, 45, 46, 104, 105, 108, 109, 112, 132, 133, 134]
        self.assertFalse(is_winning(tiles))

    def test_nine_gates(self):
        tiles = [4, 5, 6, 8, 12, 16, 20, 24, 28, 32, 36, 37, 38]
        for tile in range(1, 10):
            self.assertTrue(is_winning(tiles + [tile]))

    def test_seven_pairs(self):
        tiles = [4, 5, 20, 21, 36, 37, 52, 53, 60, 61, 108, 109, 140, 141]
        self.assertTrue(is_winning(tiles))

    def test_seven_pairs_repeat(self):
        tiles = [4, 5, 20, 21, 36, 37, 52, 53, 54, 55, 108, 109, 140, 141]
        self.assertFalse(is_winning(tiles))

    def test_four_pairs(self):
        tiles = [4, 5, 60, 61, 116, 117, 132, 133]
        self.assertFalse(is_winning(tiles))

    def test_ryanpeikou(self):
        tiles = [8, 9, 12, 13, 16, 17, 60, 61, 64, 65, 68, 69, 144, 145]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_thirteen_orphans(self):
        tiles = [4, 36, 44, 76, 77, 84, 116, 124, 128, 132, 136, 140, 144, 148]
        self.assertTrue(is_winning(tiles))

    def test_eleven_orphans(self):
        tiles = [4, 36, 44, 76, 77, 84, 116, 124, 128, 132, 133, 134, 144, 148]
        self.assertFalse(is_winning(tiles))

    def test_thirteen_orphans_and_other(self):
        tiles = [4, 36, 44, 52, 76, 84, 116, 124, 128, 132, 136, 140, 144, 148]
        self.assertFalse(is_winning(tiles))
