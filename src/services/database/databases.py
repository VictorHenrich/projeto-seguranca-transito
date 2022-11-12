from typing import Mapping, Sequence
from .database import Database
from .exceptions import DatabaseNotFoundError


class Databases:
    def __init__(self) -> None:
        self.__bases: Mapping[str, Database] = {}

    @property
    def bases(self) -> Mapping[str, Database]:
        return self.__bases

    def append_databases(self, *databases: Sequence[Database]) -> None:
        for database in databases:
            self.__bases[database.name] = database

    def get_database(self, name: str = "main") -> Database:
        try:
            return self.__bases[name]

        except KeyError:
            raise DatabaseNotFoundError()
