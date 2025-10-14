import logging

import sqlalchemy as sa
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .engine import engine
from .models import Base as Base

logger = logging.getLogger(__name__)


class SQLAlchemy:
    def __init__(self, engine: sa.Engine) -> None:
        self._Session = scoped_session(sessionmaker(engine, autobegin=False))

    @property
    def session(self) -> Session:
        return self._Session()

    def close(self) -> None:
        self._Session.remove()


db = SQLAlchemy(engine)
