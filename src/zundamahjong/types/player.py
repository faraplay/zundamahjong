from __future__ import annotations

from pydantic import BaseModel, computed_field


class Player(BaseModel, frozen=True):
    name: str
    has_account: bool = False
    new_user: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def id(self) -> str:
        return f"player:{self.name}"


class PlayerConnection(BaseModel):
    player: Player
    is_connected: bool = True
