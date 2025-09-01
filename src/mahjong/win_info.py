from enum import StrEnum
from pydantic import BaseModel

from .tile import Tile, is_number
from .call import Call, CallType
from .form_hand import formed_hand_possibilities


class Win(BaseModel):
    win_seat: int
    lose_seat: int | None
    hand: list[Tile]
    calls: list[Call]


class Yaku(StrEnum):
    EYES = "eyes"
    SEVEN_PAIRS = "seven pairs"
    THIRTEEN_ORPHANS = "thirteen orphans"


class YakuHan(BaseModel):
    yaku: Yaku
    han: int


class Score(BaseModel):
    yaku_hans: list[YakuHan]
    han_total: int
    score: int


class WinScoreInfo(BaseModel):
    win: Win
    score: Score


default_yaku_values = {Yaku.EYES: 1, Yaku.SEVEN_PAIRS: 3, Yaku.THIRTEEN_ORPHANS: 13}


class ScoringHand:
    def __init__(
        self,
        win: Win,
        yaku_values: dict[Yaku, int] = default_yaku_values,
    ):
        self._win = win
        self._yaku_values = yaku_values

    def get_score(self):
        scores = [
            ScoringFormedHand(self, formed_hand).get_score()
            for formed_hand in formed_hand_possibilities(self._win.hand)
        ]

        def score_key(score: Score):
            return (score.han_total, score.score)

        return max(scores, key=score_key)


class ScoringFormedHand:
    def __init__(self, scoring_hand: ScoringHand, formed_hand: list[Call]):
        self._scoring_hand = scoring_hand
        self._formed_hand = formed_hand

    def get_yakus(self):
        yakus: list[Yaku] = []
        for yaku, is_yaku in self.is_yaku_functions.items():
            if is_yaku(self):
                yakus.append(yaku)
        return yakus

    def get_score(self):
        yakus = self.get_yakus()
        yaku_hans = [
            YakuHan(yaku=yaku, han=self._scoring_hand._yaku_values[yaku])
            for yaku in yakus
        ]
        han_total = sum(yaku_han.han for yaku_han in yaku_hans)
        score = 2 ** min(han_total, 6)
        return Score(yaku_hans=yaku_hans, han_total=han_total, score=score)

    def _is_seven_pairs(self):
        return len(self._formed_hand) == 7 and all(
            call.call_type == CallType.PAIR for call in self._formed_hand
        )

    def _is_thirteen_orphans(self):
        return (
            len(self._formed_hand) == 1
            and self._formed_hand[0].call_type == CallType.THIRTEEN_ORPHANS
        )

    def _is_eyes(self):
        pairs = [call for call in self._formed_hand if call.call_type == CallType.PAIR]
        if len(pairs) != 1:
            return False
        tile = pairs[0]
        if not is_number(tile):
            return False
        return (tile % 10) % 3 == 2

    is_yaku_functions = {
        Yaku.EYES: _is_eyes,
        Yaku.SEVEN_PAIRS: _is_seven_pairs,
        Yaku.THIRTEEN_ORPHANS: _is_thirteen_orphans,
    }
