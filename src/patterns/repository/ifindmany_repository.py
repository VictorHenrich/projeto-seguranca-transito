from typing import Protocol, Generic, TypeVar, Sequence

from models import BaseModel


T = TypeVar("T", contravariant=True)
M = TypeVar("M", bound=BaseModel, covariant=True)


class IFindManyRepository(Protocol, Generic[T, M]):
    def list(self, params: T) -> Sequence[M]:
        ...
