from typing import (
    Protocol, 
    Generic,
    TypeVar
)


T = TypeVar('T')


class IUpdateRepository(Protocol, Generic[T]):
    def update(self, param: T) -> None:
        pass