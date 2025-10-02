from enum import IntEnum
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field

from .tile import TileId
from .meld import MeldType


class CallType(IntEnum):
    PAIR = 0
    CHI = 1
    PON = 2
    OPEN_KAN = 3
    ADD_KAN = 4
    CLOSED_KAN = 5
    THIRTEEN_ORPHANS = 6


call_meld_types = {
    CallType.PAIR: MeldType.PAIR,
    CallType.CHI: MeldType.CHI,
    CallType.PON: MeldType.PON,
    CallType.OPEN_KAN: MeldType.OPEN_KAN,
    CallType.ADD_KAN: MeldType.ADD_KAN,
    CallType.CLOSED_KAN: MeldType.CLOSED_KAN,
    CallType.THIRTEEN_ORPHANS: MeldType.THIRTEEN_ORPHANS,
}


def get_meld_type(call_type: CallType):
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
    Union[OpenCall, OpenKanCall, AddKanCall, ClosedKanCall],
    Field(discriminator="call_type"),
]


def get_call_tiles(call: Call):
    if call.call_type == CallType.CLOSED_KAN:
        return list(call.tiles)
    elif call.call_type == CallType.ADD_KAN:
        return [call.added_tile, call.called_tile] + list(call.other_tiles)
    else:
        return [call.called_tile] + list(call.other_tiles)
