from typing import (
    Protocol,
    Generic,
    TypeVar
)



T = TypeVar('T')


class IExclusionRepository(Protocol, Generic[T]):
    def delete(self, param: T) -> None:
        pass