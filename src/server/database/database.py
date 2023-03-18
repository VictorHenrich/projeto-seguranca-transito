from typing import Any, Dict, Optional, Union, Protocol, Type
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
import asyncio
from .exceptions import InstanceEngineError


class DatabaseParameters(Protocol):
    name: Optional[str]
    connection_url: str
    async_: bool = False
    debug: bool = False


class Database:
    def __init__(self, params: DatabaseParameters) -> None:
        self.__name: str = params.name or "main"
        self.__engine: Union[Engine, AsyncEngine] = self.__create_engine(params)
        self.__Base: Type[DeclarativeBase] = self.__create_base()

    @property
    def engine(self) -> Union[Engine, AsyncEngine]:
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

    def create_session(self, **options: Dict[str, Any]) -> Union[Session, AsyncSession]:
        if type(self.__engine) is Engine:
            return Session(self.__engine, **options)

        if type(self.__engine) is AsyncEngine:
            return AsyncSession(self.__engine, **options)

        else:
            raise Exception("Type engine is not defined!")

    def __create_engine(self, params: DatabaseParameters) -> Union[Engine, AsyncEngine]:
        if not params.async_:
            return create_engine(params.connection_url, echo=params.debug)

        else:
            return create_async_engine(params.connection_url, echo=params.debug)

    def migrate(self, drop_tables: bool = False) -> None:
        if type(self.__engine) is Engine:
            self.__migrate_default(drop_tables)

        else:
            asyncio.run(self.__migrate_async(drop_tables))

    def __migrate_default(self, drop_tables: bool) -> None:
        if type(self.__engine) is not Engine:
            raise InstanceEngineError()

        if drop_tables:
            self.__Base.metadata.drop_all(self.__engine)

        self.__Base.metadata.create_all(self.__engine)

    async def __migrate_async(self, drop_tables: bool) -> None:
        # if self.__engine is not AsyncEngine:
        #     raise InstanceEngineError()

        # async with self.__engine.begin() as transaction:
        #     if drop_tables:
        #         await transaction.run_sync(self.__Base.metadata.drop_all)

        #     await transaction.run_sync(self.__Base.metadata.create_all)
        pass
