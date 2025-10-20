import logging
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from flask import Flask
from flask.globals import app_ctx

from .engine import engine
from .models import Base as Base

logger = logging.getLogger(__name__)


def _app_ctx_id() -> int:
    """Get the id of the current Flask application context for the session scope."""
    return id(app_ctx._get_current_object())  # type: ignore[attr-defined]


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

    def _close(self, exc: Optional[BaseException]) -> None:
        if self._session.registry.has():
            logger.info(
                f"Closing database session within Flask application context {_app_ctx_id()}"
            )
        self._session.remove()


db = SQLAlchemy(engine)
