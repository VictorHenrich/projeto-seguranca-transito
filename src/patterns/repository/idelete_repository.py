from typing import Protocol, Generic, TypeVar, Union, Any


T = TypeVar("T")
TR = TypeVar("TR", bound=Union[None, Any])


class IDeleteRepository(Protocol, Generic[T]):
    def delete(self, params: T) -> TR:
        pass
