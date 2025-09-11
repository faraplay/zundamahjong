from pydantic import BaseModel


class Player(BaseModel, frozen=True):
    id: str
    name: str

    @classmethod
    def from_name(cls, name: str):
        return Player(id="player:" + name, name=name)
