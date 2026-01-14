from typing import ClassVar, final

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ..types.avatar import Avatar


class Base(DeclarativeBase):
    """Inherits from :py:class:`sqlalchemy.orm.DeclarativeBase`. Refer to
    `the upstream docs
    <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase>`__
    for more details.
    """

    metadata: ClassVar[MetaData]
    """`Holds information
    <https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-metadata>`__
    about the tables that are used in the database (e.g. column data types).

    ::

        from ..database import Base, engine

        # Create all needed tables in the database.
        Base.metadata.create_all(engine)

    """


@final
class User(Base):
    """Database model used to hold registered user account information."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Unique id value used as primary key."""

    name: Mapped[str] = mapped_column(unique=True)
    """Account login username."""

    password: Mapped[str] = mapped_column()
    """Hashed login password."""

    avatar: Mapped[Avatar] = mapped_column(server_default=("zundamon"))
    """User's last chosen :py:class:`.Avatar`."""
