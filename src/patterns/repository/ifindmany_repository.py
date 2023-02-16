from typing import Protocol, Generic, TypeVar, Sequence

from models import BaseModel


T = TypeVar("T")

M = TypeVar("M", bound=BaseModel)


class IFindManyRepository(Protocol, Generic[T, M]):
    def list(self, params: T) -> Sequence[M]:
        pass
