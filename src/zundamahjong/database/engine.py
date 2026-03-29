import os

from flask import Flask
from pydantic import BaseModel
from sqlalchemy import Engine, create_engine

from .models import Base


class DatabaseConfig(BaseModel):
    """Used to validate application database config parameters."""

    DB_HOST: str | None = None
    DB_NAME: str = "zundamahjong"
    DB_USER: str = "zundamahjong"
    DB_PASSWORD: str = ""

    DB_FILE: str = "debug.db"


def engine(app: Flask) -> Engine:
    """Create instance of :py:class:`sqlalchemy.Engine` based on the Flask
    application object's configuration. The value of :py:obj:`engine.url`
    the end consumer of :py:mod:`zundamahjong` and refers either to a SQLite
    on-disk database or to a database in a PostgreSQL server."""

    db_config = DatabaseConfig.model_validate(app.config)

    if db_config.DB_HOST:
        engine = create_engine(
            f"postgresql+psycopg://{db_config.DB_USER}:{db_config.DB_PASSWORD}@{db_config.DB_HOST}/{db_config.DB_NAME}?sslmode=require"
        )

    else:
        engine = create_engine(f"sqlite:///{db_config.DB_FILE}")

        if not os.path.isfile(db_config.DB_FILE):
            Base.metadata.create_all(engine)

    return engine
