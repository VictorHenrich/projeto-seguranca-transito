from typing import Protocol, Generic, TypeVar, Collection, Union, Sequence

from models import BaseModel


T = TypeVar("T", contravariant=True)
M = TypeVar("M", bound=Union[BaseModel, Sequence[BaseModel]], covariant=True)


class IFindManyRepository(Protocol, Generic[T, M]):
    def find_many(self, params: T) -> Collection[M]:
        ...
