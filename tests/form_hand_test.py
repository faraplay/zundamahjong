import unittest

from zundamahjong.mahjong.form_hand import is_winning, formed_hand_possibilities


class FormHandTest(unittest.TestCase):
    def test_wrong_size_hand(self) -> None:
        tiles = [10, 11, 12, 13]
        self.assertFalse(is_winning(tiles))

    def test_wrong_size_suits(self) -> None:
        tiles = [20, 21, 22, 23, 150, 151, 152, 153]
        self.assertFalse(is_winning(tiles))

    def test_number_pair(self) -> None:
        tiles = [50, 51]
        self.assertTrue(is_winning(tiles))

    def test_honor_pair(self) -> None:
        tiles = [310, 311]
        self.assertTrue(is_winning(tiles))

    def test_number_run(self) -> None:
        tiles = [10, 20, 30, 50, 51]
        self.assertTrue(is_winning(tiles))

    def test_number_run_unsorted(self) -> None:
        tiles = [20, 50, 30, 10, 51]
        self.assertTrue(is_winning(tiles))

    def test_number_bad_run(self) -> None:
        tiles = [10, 20, 21, 30, 40]
        self.assertFalse(is_winning(tiles))

    def test_number_triple_run(self) -> None:
        tiles = [10, 11, 12, 20, 21, 22, 30, 31, 32, 80, 81]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_number_double_run(self) -> None:
        tiles = [30, 31, 40, 41, 50, 51, 60, 61]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_honor_run(self) -> None:
        tiles = [20, 21, 310, 320, 330]
        self.assertFalse(is_winning(tiles))

    def test_number_overlapping_run(self) -> None:
        tiles = [20, 21, 30, 40, 41, 50, 51, 52, 60, 61, 70]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 1)

    def test_number_pon_run(self) -> None:
        tiles = [30, 31, 32, 40, 50, 60, 61, 62]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_many_suits_win(self) -> None:
        tiles = [40, 50, 60, 110, 111, 112, 260, 270, 271, 272, 280, 330, 331, 332]
        self.assertTrue(is_winning(tiles))

    def test_many_suits_not_win(self) -> None:
        tiles = [40, 50, 60, 110, 111, 112, 260, 261, 270, 271, 280, 330, 331, 332]
        self.assertFalse(is_winning(tiles))

    def test_nine_gates(self) -> None:
        tiles = [10, 11, 12, 20, 30, 40, 50, 60, 70, 80, 90, 91, 92]
        for tile in range(1, 10):
            self.assertTrue(is_winning(tiles + [tile]))

    def test_seven_pairs(self) -> None:
        tiles = [10, 11, 50, 51, 90, 91, 130, 131, 150, 151, 270, 271, 350, 351]
        self.assertTrue(is_winning(tiles))

    def test_seven_pairs_repeat(self) -> None:
        tiles = [10, 11, 50, 51, 90, 91, 130, 131, 132, 133, 270, 271, 350, 351]
        self.assertFalse(is_winning(tiles))

    def test_four_pairs(self) -> None:
        tiles = [10, 11, 150, 151, 290, 291, 330, 331]
        self.assertFalse(is_winning(tiles))

    def test_ryanpeikou(self) -> None:
        tiles = [20, 21, 30, 31, 40, 41, 150, 151, 160, 161, 170, 171, 360, 361]
        self.assertEqual(len(formed_hand_possibilities(tiles)), 2)

    def test_thirteen_orphans(self) -> None:
        tiles = [10, 90, 110, 190, 191, 210, 290, 310, 320, 330, 340, 350, 360, 370]
        self.assertTrue(is_winning(tiles))

    def test_eleven_orphans(self) -> None:
        tiles = [10, 90, 110, 190, 191, 210, 290, 310, 320, 330, 331, 332, 360, 370]
        self.assertFalse(is_winning(tiles))

    def test_thirteen_orphans_and_other(self) -> None:
        tiles = [10, 90, 110, 130, 190, 210, 290, 310, 320, 330, 340, 350, 360, 370]
        self.assertFalse(is_winning(tiles))
