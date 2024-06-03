"""
# Repository

Interface for interactions with database.

"""
from abc import ABC, abstractmethod
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.sqlalchemy_uow.utils import chunks

CHUNK_SIZE = 1000


class AbstractRepository(ABC):

    @abstractmethod
    def insert(self, dict_list, table):  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def truncate(self, table):  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def add(self, *args):  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def list(self, *args) -> list:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def count(self, *args) -> int:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args):  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def execute(self, statement):  # pragma: no cover
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository, ABC):
    """
    Main repository for interacting with DB.
    """

    def __init__(self, session):
        self.session = session

    def insert(self, dict_list, table) -> None:
        """
        Insert dict list into DB with bulk insert.
        """
        for item in chunks(dict_list, CHUNK_SIZE):
            try:
                self.session.bulk_insert_mappings(table, item)
            except IntegrityError:
                self.session.rollback()

    def truncate(self, table) -> None:
        """
        Truncate table.
        """
        self.session.query(table).delete()

    def add(self, item) -> None:
        """
        Add a row to a table.
        """
        self.session.add(item)

    def list(self, table, filter_: list = None) -> list:
        """
        Get data as list.
        """
        if filter_ is None:
            return self.session.query(table).yield_per(CHUNK_SIZE)
        return self.session.query(table).filter(*filter_).yield_per(CHUNK_SIZE)

    def count(self, table_col, filter_: list = None) -> int:
        """
        Count the table column by filter.
        """
        if filter_ is None:
            return self.session.query(table_col).count()
        return self.session.query(table_col).filter(*filter_).count()

    def delete(self, table, filter_: list):
        """
        Delete row of table.
        """
        self.session.query(table).filter(*filter_).delete()

    def execute(self, statement: str):
        """
        Execute statement.
        """
        return self.session.execute(text(statement)).mappings().all()
