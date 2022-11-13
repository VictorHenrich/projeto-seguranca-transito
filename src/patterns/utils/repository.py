from typing import (
    Protocol, 
    TypeVar, 
    Generic,
    Sequence,
    Mapping,
    Any,
    TypeAlias,
    Optional
)


T = TypeVar('T')

Args: TypeAlias = Sequence[Any]
Kwargs: TypeAlias = Mapping[str, Any]



class Repository(Protocol, Generic[T]):
    @staticmethod
    def create(*args: Args, **kwargs: Kwargs) -> Optional[T]:
        pass
    
    @staticmethod
    def update(*args: Args, **kwargs: Kwargs) -> Optional[T]:
        pass
    
    @staticmethod
    def delete(*args: Args, **kwargs: Kwargs) -> Optional[T]:
        pass

    @staticmethod
    def get(*args: Args, **kwargs: Kwargs) -> T:
        pass

    @staticmethod
    def list(*args: Args, **kwargs: Kwargs) -> list[T]:
        pass