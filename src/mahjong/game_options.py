from pydantic import BaseModel


class GameOptions(BaseModel):
    player_count: int = 4
    auto_replace_flowers: bool = True
    end_wall_count: int = 14
