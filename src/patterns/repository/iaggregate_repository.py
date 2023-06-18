from typing import Protocol, TypeVar, Generic, Collection, Union

from models import BaseModel


T = TypeVar("T", contravariant=True)
M = TypeVar(
    "M", bound=Collection[Union[BaseModel, Collection[BaseModel]]], covariant=True
)


class IAggregateRepository(Protocol, Generic[T, M]):
    def aggregate(self, params: T) -> M:
        ...
