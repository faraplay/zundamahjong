from pydantic import BaseModel


class PlayerInfo(BaseModel):
    player_id: str
    player: int
