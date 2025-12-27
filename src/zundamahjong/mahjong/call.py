from enum import IntEnum
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from .meld import MeldType
from .tile import TileId


class CallType(IntEnum):
    "Enum representing the type of call (chii, pon, open kan, added kan, closed kan)"

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
"Dictionary containing the meld type for each :py:class:`CallType`."


def get_meld_type(call_type: CallType) -> MeldType:
    "Returns the meld type (chii/pon/kan) of a :py:class:`CallType`."
    return call_meld_types[call_type]


class OpenCall(BaseModel, frozen=True):
    "Represents a chii or pon call."

    call_type: Literal[CallType.CHI, CallType.PON]
    "The :py:class:`CallType` of the call."
    called_player_index: int
    "The index of the player who discarded the called tile."
    called_tile: TileId
    "The :py:class:`TileId` of the called tile."
    other_tiles: tuple[TileId, TileId]
    "The other :py:class:`TileId` s used to make the meld."


class OpenKanCall(BaseModel, frozen=True):
    "Represents an open kan call."

    call_type: Literal[CallType.OPEN_KAN] = CallType.OPEN_KAN
    "The :py:class:`CallType` of the call."
    called_player_index: int
    "The index of the player who discarded the called tile."
    called_tile: TileId
    "The :py:class:`TileId` of the called tile."
    other_tiles: tuple[TileId, TileId, TileId]
    "The other :py:class:`TileId` s used to make the meld."


class AddKanCall(BaseModel, frozen=True):
    "Represents an added kan call."

    call_type: Literal[CallType.ADD_KAN] = CallType.ADD_KAN
    "The :py:class:`CallType` of the call."
    called_player_index: int
    "The index of the player who discarded the called tile."
    called_tile: TileId
    "The :py:class:`TileId` of the called tile."
    added_tile: TileId
    "The :py:class:`TileId` of the added tile."
    other_tiles: tuple[TileId, TileId]
    "The other :py:class:`TileId` s used to make the meld."


class ClosedKanCall(BaseModel, frozen=True):
    "Represents a closed kan call."

    call_type: Literal[CallType.CLOSED_KAN] = CallType.CLOSED_KAN
    "The :py:class:`CallType` of the call."
    tiles: tuple[TileId, TileId, TileId, TileId]
    "The :py:class:`TileId` s used to make the closed kan."


Call = Annotated[
    OpenCall | OpenKanCall | AddKanCall | ClosedKanCall,
    Field(discriminator="call_type"),
]
"""
Represents a call made by a player.
Contains the call type and the tiles of the call.
"""


def get_call_tiles(call: Call) -> list[TileId]:
    """
    Returns a list of the :py:class:`TileId` s that
    make up the given :py:class:`Call`.
    """
    if call.call_type == CallType.CLOSED_KAN:
        return list(call.tiles)
    elif call.call_type == CallType.ADD_KAN:
        return [call.added_tile, call.called_tile] + list(call.other_tiles)
    else:
        return sorted([call.called_tile] + list(call.other_tiles))
