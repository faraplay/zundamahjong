import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

db_host = os.getenv("DB_HOST")

if db_host:
    db_name = os.getenv("DB_NAME", "zundamahjong")
    db_user = os.getenv("DB_USER", "zundamahjong")
    db_password = os.getenv("DB_PASSWORD")

    engine = create_engine(
        f"postgresql+psycopg://{db_user}:{db_password}@{db_host}/{db_name}?sslmode=require"
    )

else:
    engine = create_engine("sqlite:///debug.db")

db_factory = sessionmaker(bind=engine)


def create_tables() -> None:
    Base.metadata.create_all(engine)


if not db_host and not os.path.isfile("debug.db"):
    create_tables()
