from enum import IntEnum
from collections.abc import Iterable, Set
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field, TypeAdapter


from .tile import TileId
from .call import OpenCall


class ActionType(IntEnum):
    PASS = 0
    CONTINUE = 1
    DRAW = 2
    DISCARD = 3
    CHII = 6
    PON = 7
    OPEN_KAN = 8
    ADD_KAN = 9
    CLOSED_KAN = 10
    FLOWER = 11
    RON = 12
    TSUMO = 13


call_action_types = {
    ActionType.CHII,
    ActionType.PON,
    ActionType.OPEN_KAN,
    ActionType.ADD_KAN,
    ActionType.CLOSED_KAN,
}


class SimpleAction(BaseModel, frozen=True):
    action_type: Literal[
        ActionType.PASS,
        ActionType.CONTINUE,
        ActionType.DRAW,
        ActionType.RON,
        ActionType.TSUMO,
    ]


class HandTileAction(BaseModel, frozen=True):
    action_type: Literal[ActionType.DISCARD, ActionType.FLOWER]
    tile: TileId


class OpenCallAction(BaseModel, frozen=True):
    action_type: Literal[
        ActionType.CHII,
        ActionType.PON,
    ]
    other_tiles: tuple[TileId, TileId]


class OpenKanAction(BaseModel, frozen=True):
    action_type: Literal[ActionType.OPEN_KAN,] = ActionType.OPEN_KAN
    other_tiles: tuple[TileId, TileId, TileId]


class AddKanAction(BaseModel, frozen=True):
    action_type: Literal[ActionType.ADD_KAN] = ActionType.ADD_KAN
    tile: TileId
    pon_call: OpenCall


class ClosedKanAction(BaseModel, frozen=True):
    action_type: Literal[ActionType.CLOSED_KAN] = ActionType.CLOSED_KAN
    tiles: tuple[TileId, TileId, TileId, TileId]


Action = Annotated[
    Union[
        SimpleAction,
        HandTileAction,
        OpenCallAction,
        OpenKanAction,
        AddKanAction,
        ClosedKanAction,
    ],
    Field(discriminator="action_type"),
]

action_adapter = TypeAdapter(Action)


class ActionList:
    def __init__(
        self, default_action: Action = SimpleAction(action_type=ActionType.PASS)
    ):
        self._actions = [default_action]

    @property
    def default(self):
        return self._actions[0]

    @property
    def auto(self):
        if len(self._actions) == 1:
            return self._actions[0]
        else:
            return None

    @property
    def actions(self) -> list[Action]:
        return self._actions

    def add_simple_action(
        self,
        action_type: Literal[
            ActionType.PASS,
            ActionType.CONTINUE,
            ActionType.DRAW,
            ActionType.RON,
            ActionType.TSUMO,
        ],
    ):
        self._actions.append(SimpleAction(action_type=action_type))

    def add_actions(self, actions: Iterable[Action]):
        self._actions.extend(actions)
