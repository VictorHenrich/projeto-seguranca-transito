from typing import (
    Generic,
    TypeVar,
    Optional,
    Sequence,
    Mapping,
    Any,
    TypeAlias
)
from abc import ABC, abstractmethod


Args: TypeAlias = Sequence[Any]
Kwargs: TypeAlias = Mapping[str, Any]

T = TypeVar('T')




class CrudRepository(ABC, Generic[T]):
    @abstractmethod
    def create(self, *args: Sequence[Any], **kwargs: Kwargs) -> Optional[T]:
        pass
    
    @abstractmethod
    def update(self, *args: Sequence[Any], **kwargs: Kwargs) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, *args: Sequence[Any], **kwargs: Kwargs) -> Optional[T]:
        pass

    @abstractmethod
    def load(self, *args: Sequence[Any], **kwargs: Kwargs) -> T:
        pass

    @abstractmethod
    def fetch(self, *args: Sequence[Any], **kwargs: Kwargs) -> list[T]:
        pass
