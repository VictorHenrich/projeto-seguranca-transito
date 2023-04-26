from typing import Protocol, Generic, TypeVar


T = TypeVar("T", covariant=True)


class IService(Protocol, Generic[T]):
    def execute(self) -> T:
        ...
