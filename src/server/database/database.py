from typing import Any, Dict, Optional, Type
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import Session


class Database:
    def __init__(
        self,
        name: Optional[str],
        connection_url: str,
        debug: bool = False,
    ) -> None:
        self.__name: str = name or "main"
        self.__engine: Engine = create_engine(connection_url, echo=debug)
        self.__Base: Type[DeclarativeBase] = self.__create_base()

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def Base(self) -> Type[DeclarativeBase]:
        return self.__Base

    @property
    def name(self) -> str:
        return self.__name

    def __create_base(self) -> Type[DeclarativeBase]:
        class Base(DeclarativeBase):
            pass

        return Base

    def create_session(self, **options: Dict[str, Any]) -> Session:
        return Session(self.__engine, **options)

    def migrate(self, drop_tables: bool = False) -> None:
        if drop_tables:
            self.__Base.metadata.drop_all(self.__engine)

        self.__Base.metadata.create_all(self.__engine)
