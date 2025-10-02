from enum import IntEnum
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field

from .tile import TileId


class CallType(IntEnum):
    PAIR = 0
    CHI = 1
    PON = 2
    OPEN_KAN = 3
    ADD_KAN = 4
    CLOSED_KAN = 5
    THIRTEEN_ORPHANS = 6


class OpenCall(BaseModel, frozen=True):
    call_type: Literal[CallType.CHI, CallType.PON]
    called_player_index: int
    called_tile: TileId
    other_tiles: tuple[TileId, TileId]


class OpenKanCall(BaseModel, frozen=True):
    call_type: Literal[CallType.OPEN_KAN] = CallType.OPEN_KAN
    called_player_index: int
    called_tile: TileId
    other_tiles: tuple[TileId, TileId, TileId]


class AddKanCall(BaseModel, frozen=True):
    call_type: Literal[CallType.ADD_KAN] = CallType.ADD_KAN
    called_player_index: int
    called_tile: TileId
    added_tile: TileId
    other_tiles: tuple[TileId, TileId]


class ClosedKanCall(BaseModel, frozen=True):
    call_type: Literal[CallType.CLOSED_KAN] = CallType.CLOSED_KAN
    tiles: tuple[TileId, TileId, TileId, TileId]


Call = Annotated[
    Union[OpenCall, OpenKanCall, AddKanCall, ClosedKanCall],
    Field(discriminator="call_type"),
]
