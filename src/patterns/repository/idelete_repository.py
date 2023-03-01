from typing import Protocol, Generic, TypeVar, Union, Any


T = TypeVar("T", contravariant=True)
TR = TypeVar("TR", bound=Union[None, Any], covariant=True)


class IDeleteRepository(Protocol, Generic[T, TR]):
    def delete(self, params: T) -> TR:
        ...
