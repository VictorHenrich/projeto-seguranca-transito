from typing import Protocol, TypeVar, Generic

from models import BaseModel


T = TypeVar("T")

M = TypeVar("M", bound=BaseModel)


class IFindRepository(Protocol, Generic[T, M]):
    def get(self, params: T) -> M:
        pass
