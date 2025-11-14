import datetime
import uuid
from typing import final

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON

from ..mahjong.call import Call
from ..mahjong.tile import TileId
from ..types.avatar import Avatar


class Base(DeclarativeBase):
    pass


@final
class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    password: Mapped[str] = mapped_column()
    """Hashed user password."""

    avatar: Mapped[Avatar] = mapped_column(server_default=("zundamon"))
    """User's chosen avatar."""


@final
class Round(Base):
    """Game round as stored in the database."""

    __tablename__ = "round"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    """Unique id value for the game round."""

    start_time: Mapped[datetime.datetime] = mapped_column()
    """Time at which the game round began."""


@final
class Win(Base):
    """Round win as stored in the database.

    Refer to the `round` table for such information as the number of players, their
    names, their order around the table, and other information about the environment.
    """

    __tablename__ = "round_win"

    round: Mapped[uuid.UUID] = mapped_column(ForeignKey("round.id"), primary_key=True)
    """Game round that this winning hand corresponds to."""

    win_player: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    """Account Id of the winning player.

    We don't store anonymous players' wins in this table, though such information
    may be recovered from the `round` table.
    """

    is_tsumo: Mapped[bool] = mapped_column()

    hand: Mapped[list[TileId]] = mapped_column(type_=JSON)
    calls: Mapped[list[Call]] = mapped_column(type_=JSON)
    flowers: Mapped[list[TileId]] = mapped_column(type_=JSON)

    after_flower_count: Mapped[int] = mapped_column()
    after_kan_count: Mapped[int] = mapped_column()

    is_chankan: Mapped[bool] = mapped_column()
    is_haitei: Mapped[bool] = mapped_column()
    is_houtei: Mapped[bool] = mapped_column()
    is_tenhou: Mapped[bool] = mapped_column()
    is_chiihou: Mapped[bool] = mapped_column()
