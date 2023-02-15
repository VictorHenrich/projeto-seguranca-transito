from typing import (
    Protocol,
    Generic,
    TypeVar,
    TypeAlias,
    Sequence,
    Mapping,
    Optional,
    Any,
)


Args: TypeAlias = Sequence[Any]

Kwargs: TypeAlias = Mapping[str, Any]

T = TypeVar("T")


class IService(Protocol, Generic[T]):
    def execute(self, *args: Args, **kwargs: Kwargs) -> T:
        pass
