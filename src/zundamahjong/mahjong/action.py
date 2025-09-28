from enum import IntEnum
from collections.abc import Set
from pydantic import BaseModel

from .tile import Tile


class ActionType(IntEnum):
    PASS = 0
    CONTINUE = 1
    DRAW = 2
    DISCARD = 3
    CHI_A = 4
    CHI_B = 5
    CHI_C = 6
    PON = 7
    OPEN_KAN = 8
    ADD_KAN = 9
    CLOSED_KAN = 10
    FLOWER = 11
    RON = 12
    TSUMO = 13


call_action_types = {
    ActionType.CHI_A,
    ActionType.CHI_B,
    ActionType.CHI_C,
    ActionType.PON,
    ActionType.OPEN_KAN,
    ActionType.ADD_KAN,
    ActionType.CLOSED_KAN,
}


class Action(BaseModel, frozen=True):
    action_type: ActionType
    tile: Tile = 0


class ActionSet:
    def __init__(self, action_type: ActionType = ActionType.PASS, tile: Tile = 0):
        self._default = Action(action_type=action_type, tile=tile)
        self._actions = {self._default}

    @property
    def default(self):
        return self._default

    @property
    def auto(self):
        if len(self._actions) == 1 and self._default.action_type != ActionType.DISCARD:
            return self._default
        else:
            return None

    @property
    def actions(self) -> Set[Action]:
        return self._actions

    def add(self, action_type: ActionType, tile: Tile = 0):
        self._actions.add(Action(action_type=action_type, tile=tile))
