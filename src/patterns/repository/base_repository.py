from abc import ABC
from typing import Union, TypeAlias
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession




SessionArg: TypeAlias = Union[Session, AsyncSession]


class BaseRepository(ABC):
    def __init__(self, session: SessionArg) -> None:
        self.__session: SessionArg = session

    @property
    def session(self) -> SessionArg:
        return self.__session