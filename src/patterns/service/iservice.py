from typing import (
    Protocol,
    Generic,
    TypeVar,
    TypeAlias,
    Sequence,
    Mapping,
    Union,
    Any,
)


Args: TypeAlias = Sequence[Any]

Kwargs: TypeAlias = Mapping[str, Any]

T = TypeVar("T", bound=Union[None, Any])


class IService(Protocol, Generic[T]):
    def execute(self, *args: Args, **kwargs: Kwargs) -> T:
        pass
