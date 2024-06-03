# pylint: disable=attribute-defined-outside-init
"""
# Unit of Work

Interface to repository.

With help of this module the tool is independent of the database.
"""
from abc import ABC, abstractmethod

from src.sqlalchemy_uow.repository import AbstractRepository, SqlAlchemyRepository


class AbstractUnitOfWork(ABC):
    items: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def rollback(self):  # pragma: no cover
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork, ABC):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.items = SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
