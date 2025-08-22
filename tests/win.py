import unittest

from src.mahjong.win import is_winning


class WinTest(unittest.TestCase):
    def test_wrong_size_hand(self):
        tiles = [1, 1, 12, 12]
        self.assertFalse(is_winning(tiles))

    def test_number_pair(self):
        tiles = [5, 5]
        self.assertTrue(is_winning(tiles))
