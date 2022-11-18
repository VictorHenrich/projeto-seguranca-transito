from typing import (
    Generic,
    TypeVar,
    Sequence,
    Mapping,
    Any,
    TypeAlias
)
from abc import ABC, abstractmethod


Args: TypeAlias = Sequence[Any]
Kwargs: TypeAlias = Mapping[str, Any]

T = TypeVar('T')



class AuthRepository(ABC, Generic[T]):
    @abstractmethod
    def auth(self, *args: Args, **kwargs: Kwargs) -> T:
        pass