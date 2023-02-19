from typing import Protocol, Generic, TypeVar, Union, Any


T = TypeVar("T")
TR = TypeVar("TR", bound=Union[None, Any])


class IUpdateRepository(Protocol, Generic[T]):
    def update(self, params: T) -> TR:
        pass
