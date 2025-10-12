from typing import final

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ..types.avatar import Avatar


class Base(DeclarativeBase):
    pass


@final
class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    """Hashed user password."""
    password: Mapped[str] = mapped_column()

    """User's chosen avatar."""
    avatar: Mapped[Avatar] = mapped_column(server_default=("zundamon"))
