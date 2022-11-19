from typing import (
    Generic,
    TypeVar,
    Optional,
    Sequence,
    Mapping,
    Any,
    TypeAlias,
    Protocol
)


Args: TypeAlias = Sequence[Any]
Kwargs: TypeAlias = Mapping[str, Any]

T = TypeVar('T')




class CrudRepository(Protocol, Generic[T]):
    def create(self, *args: Sequence[Any], **kwargs: Kwargs) -> Optional[T]:
        pass
    
    def update(self, *args: Sequence[Any], **kwargs: Kwargs) -> Optional[T]:
        pass

    def delete(self, *args: Sequence[Any], **kwargs: Kwargs) -> Optional[T]:
        pass

    def load(self, *args: Sequence[Any], **kwargs: Kwargs) -> T:
        pass

    def fetch(self, *args: Sequence[Any], **kwargs: Kwargs) -> list[T]:
        pass
