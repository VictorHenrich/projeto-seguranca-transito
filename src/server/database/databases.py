from __future__ import annotations
from typing import (
    Mapping, 
    Sequence, 
    Optional,
    Union
)
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
from .idatabase import IDatabase
from .exceptions import DatabaseNotFoundError


class Databases:
    def __init__(self) -> None:
        self.__bases: Mapping[str, IDatabase] = {}

    @property
    def bases(self) -> Mapping[str, IDatabase]:
        return self.__bases

    def get_database(self, database_name: Optional[str] = None) -> IDatabase:
        try:
            if not database_name:
                return list(self.__bases.values())[0]

            else:
                return self.__bases[database_name]

        except KeyError:
            raise DatabaseNotFoundError()

        except IndexError:
            raise Exception('Databases is Empty!')

    def create_session(self, database_name: Optional[str] = None, **options) -> Union[Session, AsyncSession]:
        return self\
                .get_database(database_name)\
                .create_session(**options)

    def migrate(self, drop_tables: bool, database_name: Optional[str] = None) -> None:
        self\
            .get_database(database_name)\
            .migrate(drop_tables)

    def migrate_all(self, drop_tables: bool) -> None:
        for base_name in self.__bases.keys():
            self.migrate(drop_tables, base_name)

    def append_databases(self, *databases: Sequence[IDatabase]) -> None:
        for database in databases:
            self.__bases[database.name] = database
