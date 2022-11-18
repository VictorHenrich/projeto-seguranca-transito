from typing import (
    Protocol,
    TypeVar,
    Generic
)



T = TypeVar('T')


class InterfaceService(Protocol, Generic[T]):
    def execute(self, param: T) -> None:
        pass