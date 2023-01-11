from typing import (
    Protocol, 
    Generic,
    TypeVar
)


T = TypeVar('T')


class ICreationRepository(Protocol, Generic[T]):
    def create(self, param: T) -> None:
        pass
