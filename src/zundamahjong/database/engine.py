import logging
import os

from sqlalchemy import create_engine

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
    db_file = os.getenv("DB_FILE", "debug.db")

    engine = create_engine(f"sqlite:///{db_file}")

    if not os.path.isfile(db_file):
        Base.metadata.create_all(engine)
