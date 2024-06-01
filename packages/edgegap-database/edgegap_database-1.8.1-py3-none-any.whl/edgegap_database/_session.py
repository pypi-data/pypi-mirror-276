import logging
from contextlib import contextmanager
from typing import NewType

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from ._configuration import DatabaseConfiguration
from ._engine import DatabaseEngine

logger = logging.getLogger(__name__)


ReadSession = NewType('ReadSession', Session)
WriteSession = NewType('WriteSession', Session)


class DatabaseSession:
    @staticmethod
    @contextmanager
    def get_write_session(configuration: DatabaseConfiguration):
        engine = DatabaseEngine(configuration).get_engine_write_engine()
        session_factory = sessionmaker(class_=Session, bind=engine)

        with session_factory() as session:
            yield session

    @staticmethod
    @contextmanager
    def get_read_session(configuration: DatabaseConfiguration):
        engine = DatabaseEngine(configuration).get_read_engine()
        session_factory = sessionmaker(class_=Session, bind=engine, future=True)

        with session_factory() as session:
            yield session
