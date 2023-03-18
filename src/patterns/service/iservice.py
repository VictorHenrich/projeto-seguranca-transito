from typing import Protocol, Generic, TypeVar, Union, Any, Optional


T = TypeVar("T", contravariant=True)
TR = TypeVar("TR", covariant=True)


class IService(Protocol, Generic[T, TR]):
    def execute(self, props: T) -> TR:
        ...
