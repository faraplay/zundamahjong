from enum import IntEnum
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from .meld import MeldType
from .tile import TileId


class CallType(IntEnum):
    CHI = 0
    PON = 1
    OPEN_KAN = 2
    ADD_KAN = 3
    CLOSED_KAN = 4


call_meld_types = {
    CallType.CHI: MeldType.CHI,
    CallType.PON: MeldType.PON,
    CallType.OPEN_KAN: MeldType.KAN,
    CallType.ADD_KAN: MeldType.KAN,
    CallType.CLOSED_KAN: MeldType.KAN,
}


def get_meld_type(call_type: CallType) -> MeldType:
    return call_meld_types[call_type]


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
    OpenCall | OpenKanCall | AddKanCall | ClosedKanCall,
    Field(discriminator="call_type"),
]


def get_call_tiles(call: Call) -> list[TileId]:
    if call.call_type == CallType.CLOSED_KAN:
        return list(call.tiles)
    elif call.call_type == CallType.ADD_KAN:
        return [call.added_tile, call.called_tile] + list(call.other_tiles)
    else:
        return sorted([call.called_tile] + list(call.other_tiles))
