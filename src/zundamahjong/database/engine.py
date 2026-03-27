import os

from sqlalchemy import Engine, create_engine

from .models import Base

db_host = os.getenv("DB_HOST")

engine: Engine
"""Global instance of :py:class:`sqlalchemy.Engine` used to communicate
with the database. The value of :py:obj:`engine.url` is as configured by
the end consumer of :py:mod:`zundamahjong` and refers either to a SQLite
on-disk database or to a database in a PostgreSQL server."""


if db_host:
    db_name = os.getenv("DB_NAME", "zundamahjong")
    db_user = os.getenv("DB_USER", "zundamahjong")
    db_password = os.getenv("DB_PASSWORD")

    engine = create_engine(
        f"postgresql+psycopg://{db_user}:{db_password}@{db_host}/{db_name}?sslmode=require"
    )

else:
    db_file = os.getenv("DB_FILE", "debug.db")

    if db_file != ":memory:":
        engine = create_engine(f"sqlite:///{db_file}")
    else:
        engine = create_engine("sqlite://")

    if not os.path.isfile(db_file):
        Base.metadata.create_all(engine)
