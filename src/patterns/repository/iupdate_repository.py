from typing import Protocol, Generic, TypeVar, Union, Any


T = TypeVar("T", contravariant=True)
TR = TypeVar("TR", bound=Union[None, Any], covariant=True)


class IUpdateRepository(Protocol, Generic[T, TR]):
    def update(self, params: T) -> TR:
        ...
