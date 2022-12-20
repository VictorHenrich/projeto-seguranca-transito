from typing import (
    Protocol,
    Generic,
    TypeVar,
    Sequence
)
from sqlalchemy.orm.decl_api import DeclarativeMeta


T = TypeVar('T')

M = TypeVar('M', bound=DeclarativeMeta)


class IListingRepository(Protocol, Generic[T, M]):
    def list(self, param: T) -> Sequence[M]:
        pass