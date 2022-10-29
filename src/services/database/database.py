from typing import Any, Mapping, Optional, Union, Protocol
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from .exceptions import ExceptionInstanceEngine


class DatabaseParameters(Protocol):
    name: Optional[str]
    connection_url: str
    async_: bool = False
    debug: bool = False


class Database:
    def __init__(self, params: DatabaseParameters) -> None:
        self.__name: str = params.name or "main"
        self.__engine: Union[Engine, AsyncEngine] = self.__create_engine(params)
        self.__Model = declarative_base(self.__engine)

    @property
    def engine(self) -> Union[Engine, AsyncEngine]:
        return self.__engine

    @property
    def Model(self):
        return self.__Model

    @property
    def name(self) -> str:
        return self.__name

    def create_session(self, **options: Mapping[str, Any]) -> Union[Session, AsyncSession]:
        return sessionmaker(
            self.__engine,
            Session if self.__engine is Engine else AsyncSession,
            **options
        )()

    def __create_engine(self, params: DatabaseParameters) -> Union[Engine, AsyncEngine]:
        if not params.async_:
            return create_engine(params.connection_url, echo=params.debug)

        else:
            return create_async_engine(params.connection_url, echo=params.debug)

    def migrate(self, drop_tables: bool = False) -> None:
        if self.__engine is Engine:
            self.__migrate_default(drop_tables)

        else:
            self.__migrate_async(drop_tables)

    def __migrate_default(self, drop_tables: bool) -> None:
        if self.__engine is not Engine:
            raise ExceptionInstanceEngine()

        if drop_tables:
            self.__Model.metadata.drop_all(self.__engine)

        self.__Model.metadata.create_all(self.__engine)

    async def __migrate_async(self, drop_tables: bool) -> None:
        if self.__engine is not AsyncEngine:
            raise ExceptionInstanceEngine()
            
        async with self.__engine.begin() as transaction:
            if drop_tables:
                await transaction.run_sync(self.__Model.metadata.drop_all)

            await transaction.run_sync(self.__Model.metadata.create_all)
