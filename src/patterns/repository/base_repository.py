from abc import ABC
from server.database import Database


class BaseRepository(ABC):
    def __init__(self, database: Database) -> None:
        self.__database: Database = database

    @property
    def database(self) -> Database:
        return self.__database