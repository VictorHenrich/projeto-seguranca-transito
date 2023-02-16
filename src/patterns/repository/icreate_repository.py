from typing import Protocol, Generic, TypeVar, Any, Union


T = TypeVar("T")
TR = TypeVar("TR", bound=Union[None, Any])


class ICreateRepository(Protocol, Generic[T, TR]):
    def create(self, params: T) -> TR:
        pass
