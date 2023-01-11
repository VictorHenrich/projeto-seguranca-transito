from typing import (
    Protocol,
    Generic,
    TypeVar
)
from sqlalchemy.orm.decl_api import DeclarativeMeta


T = TypeVar('T')

M = TypeVar('M', bound=DeclarativeMeta)


class IAuthRepository(Protocol, Generic[T, M]):
    def auth(self, param: T) -> M:
        pass