from typing import Any, Collection, Optional, List
from sqlalchemy.orm.session import Session
from .database import Database
from exceptions import DatabaseNotFoundError


class Databases:
    __bases: List[Database] = []

    @classmethod
    def get_all(cls) -> Collection[Database]:
        return cls.__bases

    @classmethod
    def get_database(cls, database_name: str = "main") -> Database:
        if not cls.__bases:
            raise DatabaseNotFoundError(empty=True)

        try:
            return [
                database for database in cls.__bases if database.name == database_name
            ][0]

        except IndexError:
            raise DatabaseNotFoundError()

    @classmethod
    def create_session(cls, database_name: str = "main", **options: Any) -> Session:
        return cls.get_database(database_name).create_session(**options)

    @classmethod
    def migrate(cls, drop_tables: bool, database_name: str = "main") -> None:
        cls.get_database(database_name).migrate(drop_tables)

    @classmethod
    def migrate_all(cls, drop_tables: bool) -> None:
        for database in cls.__bases:
            cls.migrate(drop_tables, database.name)

    @classmethod
    def append_databases(cls, *databases: Database) -> None:
        for database in databases:
            cls.__bases.append(database)
