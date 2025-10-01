import logging
import os

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from ..server.sio import sio

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)


engine = create_engine("sqlite:///debug.db")
db_factory = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


if not os.path.isfile("debug.db"):
    create_tables()


def get_db(sid: str) -> Session:
    with sio.session(sid) as session:
        if "db" not in session:
            session["db"] = db_factory()
        return session["db"]
