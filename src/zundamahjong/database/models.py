from typing import ClassVar, final

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ..types.avatar import Avatar


class Base(DeclarativeBase):
    """TODO"""

    metadata: ClassVar[MetaData]
    """TODO

    Example usage::

        from ..database import Base, engine

        # Populate database with tables.
        Base.metadata.create_all(engine)

    """


@final
class User(Base):
    """TODO"""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Unique id value used as primary key."""

    name: Mapped[str] = mapped_column(unique=True)
    """User's chosen login name."""

    password: Mapped[str] = mapped_column()
    """User's hashed password."""

    avatar: Mapped[Avatar] = mapped_column(server_default=("zundamon"))
    """User's chosen avatar."""
