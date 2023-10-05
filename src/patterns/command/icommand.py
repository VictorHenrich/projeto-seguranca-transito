from typing import Protocol, Generic, TypeVar

T = TypeVar("T", contravariant=True)


class ICommand(Protocol, Generic[T]):
    @property
    def name(self) -> str:
        ...

    def execute(self, props: T) -> None:
        ...
