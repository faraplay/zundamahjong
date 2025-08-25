from enum import IntEnum
from typing import NamedTuple
from collections.abc import Set

from .tile import Tile


class ActionType(IntEnum):
    NOTHING = 0
    DRAW = 1
    DISCARD = 2
    CHI_A = 3
    CHI_B = 4
    CHI_C = 5
    PON = 6
    OPEN_KAN = 7
    ADD_KAN = 8
    CLOSED_KAN = 9
    RON = 10
    TSUMO = 11


class Action(NamedTuple):
    action_type: ActionType
    tile: Tile = 0


class ActionSet:
    def __init__(self, action_type: ActionType = ActionType.NOTHING, tile: Tile = 0):
        self._default = Action(action_type, tile)
        self._actions = {self._default}

    @property
    def default(self):
        return self._default

    @property
    def actions(self) -> Set[Action]:
        return self._actions

    def add(self, action_type: ActionType, tile: Tile = 0):
        self._actions.add(Action(action_type, tile))
