from typing import Protocol, Generic, TypeVar, Any, Union


T = TypeVar("T", contravariant=True)
TR = TypeVar("TR", bound=Union[None, Any], covariant=True)


class ICreateRepository(Protocol, Generic[T, TR]):
    def create(self, params: T) -> TR:
        ...
