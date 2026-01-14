# pyright: reportIgnoreCommentWithoutRule=false

import logging
from typing import final

import sqlalchemy as sa
from flask import Flask
from flask.globals import app_ctx
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .engine import engine
from .models import Base

logger = logging.getLogger(__name__)


def _app_ctx_id() -> int:
    """Get the id of the current Flask application context object."""

    # Flask lies about `app_ctx`: it's not an instance of `AppContext` but
    # of `LocalProxy[AppContext]`, which confuses type checkers here.

    return id(app_ctx._get_current_object())  # type: ignore  # pyright: ignore


@final
class SQLAlchemy:
    """Helper class to manage SQLAlchemy ORM sessions for the server.

    :param engine: Instance of :py:class:`sqlalchemy.Engine` used to start new
                   connections to the application database. Will typically
                   refer to a local SQLite file or to a remote PostgreSQL
                   database server.
    """

    def __init__(self, engine: sa.Engine) -> None:
        self._session = scoped_session(sessionmaker(engine), _app_ctx_id)

    def init_app(self, app: Flask) -> None:
        """TODO"""

        if "sqlalchemy" in app.extensions:
            raise Exception("SQLAlchemy extension has already been initialized!")
        app.extensions["sqlalchemy"] = self

        app.teardown_appcontext(self._close)

    @property
    def session(self) -> Session:
        """Handle to an ORM session open in the current Flask application context."""

        if not self._session.registry.has():
            logger.info(
                f"Opening database session within Flask application context {_app_ctx_id()}"
            )
        return self._session()

    def _close(self, exc: BaseException | None) -> None:
        """Close ORM session (if any) in the current Flask application context."""

        if self._session.registry.has():
            logger.info(
                f"Closing database session within Flask application context {_app_ctx_id()}"
            )
        self._session.remove()


db = SQLAlchemy(engine)
""" Global instance of :py:class:`SQLAlchemy` for use in other modules.
    Built using :py:obj:`engine`.

    Example usage::

        from ..database import db
        from ..database.models import User

        with db.session.begin():
            db.session.add(User(name="Zundamon", password=password))
        # commits the transaction

"""


__all__ = ["Base", "db", "engine", "SQLAlchemy"]
