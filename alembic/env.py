import logging
from zundamahjong.database import Base, engine
from alembic import context


def init_logging() -> None:
    logger = logging.getLogger()

    generic_formatter = logging.Formatter(
        fmt="%(levelname)s [%(name)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(generic_formatter)

    logging.getLogger("alembic").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logger.addHandler(console_handler)


if not logging.getLogger().hasHandlers():
    init_logging()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    context.configure(
        url=engine.url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
