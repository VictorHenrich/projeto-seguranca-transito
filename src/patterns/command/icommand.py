from typing import Protocol, Generic, TypeVar, Union, Any


T = TypeVar("T", bound=Union[None, Any])
TR = TypeVar("TR", bound=Union[None, Any])


class ICommand(Protocol, Generic[T, TR]):
    name: str

    def execute(self, props: T) -> TR:
        pass
