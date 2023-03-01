from typing import Protocol, TypeVar, Generic

from models import BaseModel


T = TypeVar("T", contravariant=True)
M = TypeVar("M", bound=BaseModel, covariant=True)


class IFindRepository(Protocol, Generic[T, M]):
    def get(self, params: T) -> M:
        ...
