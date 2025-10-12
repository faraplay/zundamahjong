from __future__ import annotations
from pydantic import BaseModel, Field


class Player(BaseModel):
    id: str = Field(frozen=True)
    name: str = Field(frozen=True)

    logged_in: bool = False
    new_account: bool = False

    @classmethod
    def from_name(cls, name: str) -> Player:
        return Player(id="player:" + name, name=name)


class PlayerConnection(BaseModel):
    player: Player
    is_connected: bool = True
