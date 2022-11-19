from typing import (
    Protocol,
    TypeVar,
    Generic,
    Any
)



T = TypeVar('T')


class InterfaceService(Protocol, Generic[T]):
    def execute(self, param: T) -> Any:
        pass