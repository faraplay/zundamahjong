from alembic import command
from alembic.config import Config
import sqlalchemy as sa

from zundamahjong.database import Base, engine

alembic_cfg = Config(toml_file="pyproject.toml")
alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))


if __name__ == "__main__":
    if sa.inspect(engine).has_table("alembic_version"):
        raise Exception(f"Database at {engine.url} is already populated!")

    else:
        Base.metadata.create_all(engine)
        command.stamp(alembic_cfg, "head")
