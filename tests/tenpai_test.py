import unittest

from zundamahjong.mahjong.shanten import get_waits


class TenpaiTest(unittest.TestCase):
    def test_not_tenpai(self) -> None:
        self.assertSetEqual(
            get_waits([1, 2, 4, 5, 6, 13, 14, 14, 15, 15, 16, 31, 32]), frozenset()
        )

    def test_four_of_a_kind(self) -> None:
        self.assertSetEqual(
            get_waits([2, 2, 2, 2]),
            {2},
        )

    def test_ryanmen(self) -> None:
        self.assertSetEqual(
            get_waits([4, 5, 31, 31]),
            {3, 6},
        )

    def test_shanpon(self) -> None:
        self.assertSetEqual(
            get_waits([4, 4, 19, 19]),
            {4, 19},
        )

    def test_kanchan(self) -> None:
        self.assertSetEqual(
            get_waits([3, 5, 31, 31]),
            {4},
        )

    def test_penchan(self) -> None:
        self.assertSetEqual(
            get_waits([8, 9, 31, 31]),
            {7},
        )

    def test_tanki(self) -> None:
        self.assertSetEqual(
            get_waits([31]),
            {31},
        )

    def test_nakabukure(self) -> None:
        self.assertSetEqual(
            get_waits([3, 4, 4, 5]),
            {4},
        )

    def test_nobetan(self) -> None:
        self.assertSetEqual(
            get_waits([2, 3, 4, 5]),
            {2, 5},
        )

    def test_sanmenchan(self) -> None:
        self.assertSetEqual(
            get_waits([2, 3, 4, 5, 6, 31, 31]),
            {1, 4, 7},
        )

    def test_sanmentan(self) -> None:
        self.assertSetEqual(
            get_waits([2, 3, 4, 5, 6, 7, 8]),
            {2, 5, 8},
        )

    def test_sanmen_shanpon(self) -> None:
        self.assertSetEqual(
            get_waits([4, 4, 5, 5, 6, 6, 7, 7, 31, 31]),
            {4, 7, 31},
        )

    def test_entotsu(self) -> None:
        self.assertSetEqual(
            get_waits([4, 5, 6, 6, 6, 31, 31]),
            {3, 6, 31},
        )

    def test_aryanmen(self) -> None:
        self.assertSetEqual(
            get_waits([6, 7, 8, 8]),
            {5, 8},
        )

    def test_ryantan(self) -> None:
        self.assertSetEqual(
            get_waits([4, 5, 5, 5]),
            {3, 4, 6},
        )

    def test_pentan(self) -> None:
        self.assertSetEqual(
            get_waits([1, 2, 2, 2]),
            {1, 3},
        )

    def test_kantan(self) -> None:
        self.assertSetEqual(
            get_waits([5, 7, 7, 7]),
            {5, 6},
        )

    def test_kantankan(self) -> None:
        self.assertSetEqual(
            get_waits([3, 3, 3, 5, 7, 7, 7]),
            {4, 5, 6},
        )

    def test_goren_toitsu(self) -> None:
        self.assertSetEqual(
            get_waits([5, 5, 6, 6, 7, 7, 8, 8, 9, 9]),
            {5, 6, 8, 9},
        )

    def test_tatsumaki(self) -> None:
        self.assertSetEqual(
            get_waits([6, 6, 6, 7, 8, 8, 8]),
            {5, 6, 7, 8, 9},
        )

    def test_happoubijin(self) -> None:
        self.assertSetEqual(
            get_waits([2, 2, 2, 3, 4, 5, 6, 7, 7, 7]),
            {1, 2, 3, 4, 5, 6, 7, 8},
        )

    def test_seven_pairs(self) -> None:
        self.assertSetEqual(
            get_waits([1, 1, 3, 3, 5, 5, 8, 8, 11, 11, 14, 14, 15]),
            {15},
        )

    def test_thirteen_orphans(self) -> None:
        self.assertSetEqual(
            get_waits([1, 9, 9, 11, 19, 21, 31, 32, 33, 34, 35, 36, 37]),
            {29},
        )

    def test_thirteen_orphans_thirteen_wait(self) -> None:
        self.assertSetEqual(
            get_waits([1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37]),
            {1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37},
        )
