from typing import (
    Protocol,
    Generic,
    TypeVar,
    TypeAlias,
    Tuple,
    Dict,
    Union,
    Any,
)


Args: TypeAlias = Tuple[Any, ...]

Kwargs: TypeAlias = Dict[str, Any]

T = TypeVar("T", bound=Union[None, Any], covariant=True)


class IService(Protocol, Generic[T]):
    def execute(self, *args: Args, **kwargs: Kwargs) -> T:
        ...
