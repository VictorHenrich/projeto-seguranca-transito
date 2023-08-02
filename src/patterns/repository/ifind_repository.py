from typing import Protocol, TypeVar, Generic, Union, Sequence

from models import BaseModel


T = TypeVar("T", contravariant=True)
M = TypeVar("M", bound=Union[BaseModel, Sequence[BaseModel]], covariant=True)


class IFindRepository(Protocol, Generic[T, M]):
    def find_one(self, params: T) -> M:
        ...
