from typing import Protocol, TypeVar, Generic
from sqlalchemy.orm.decl_api import DeclarativeMeta


T = TypeVar("T")

M = TypeVar("M", bound=DeclarativeMeta)


class IFindRepository(Protocol, Generic[T, M]):
    def get(self, params: T) -> M:
        pass
