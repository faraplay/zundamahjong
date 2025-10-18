import sqlalchemy as sa
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .engine import engine
from .models import Base as Base


class SQLAlchemy:
    """Helper class to manage SQLAlchemy ORM sessions for the game server.

    :param engine:
    :type engine: `sqlalchemy.Engine`_

    Example usage::

        from ..database import db
        from ..database.models import User

        with db.session.begin():
            db.session.add(User(name="Zundamon", password=password))
        # commits the transaction

    """

    def __init__(self, engine: sa.Engine) -> None:
        self._Session = scoped_session(sessionmaker(engine, autobegin=False))

    @property
    def session(self) -> Session:
        """Handle to an ORM session open for the current Python thread.

        :rtype: `sqlalchemy.orm.Session`_

        """

        return self._Session()

    def close(self) -> None:
        """Close ORM session (if any) for the current Python thread. In
        practice this means keeping track of one ORM session per connected
        Socket.IO client.

        """

        self._Session.remove()


db = SQLAlchemy(engine)
