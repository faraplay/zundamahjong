# pyright: reportIgnoreCommentWithoutRule=false

import logging
from typing import final

import sqlalchemy as sa
from flask import Flask
from flask.globals import app_ctx
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .engine import engine
from .models import Base as Base

logger = logging.getLogger(__name__)


def _app_ctx_id() -> int:
    """Get the id of the current Flask application context object."""

    # Flask lies about `app_ctx`: it's not an instance of `AppContext` but
    # of `LocalProxy[AppContext]`, which confuses type checkers here.

    return id(app_ctx._get_current_object())  # type: ignore  # pyright: ignore


@final
class SQLAlchemy:
    def __init__(self, engine: sa.Engine) -> None:
        self._session = scoped_session(sessionmaker(engine), _app_ctx_id)

    def init_app(self, app: Flask) -> None:
        if "sqlalchemy" in app.extensions:
            raise Exception("SQLAlchemy extension has already been initialized!")
        app.extensions["sqlalchemy"] = self

        app.teardown_appcontext(self._close)

    @property
    def session(self) -> Session:
        if not self._session.registry.has():
            logger.info(
                f"Opening database session within Flask application context {_app_ctx_id()}"
            )
        return self._session()

    def _close(self, exc: BaseException | None) -> None:
        if self._session.registry.has():
            logger.info(
                f"Closing database session within Flask application context {_app_ctx_id()}"
            )
        self._session.remove()


db = SQLAlchemy(engine)
