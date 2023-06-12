from typing import (
    Any,
    Mapping,
    Optional,
    Callable,
    TypeAlias,
    TypeVar,
    Generic,
    Optional,
)
from abc import ABC, abstractmethod

from exceptions import MiddlewareErrorValue


T = TypeVar("T")

HandlerReturn: TypeAlias = Optional[Mapping[str, Any]]
Method: TypeAlias = Callable[[Any], Any]
Decorator: TypeAlias = Callable[[Method], Method]


class SocketMiddleware(ABC, Generic[T]):
    @abstractmethod
    def handle(self, props: Optional[T]) -> HandlerReturn:
        ...

    def catch(self, exception: Exception) -> None:
        raise exception

    def apply(self, props: Optional[T] = None) -> Decorator:
        def decorator(target: Method) -> Method:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    handler_return: HandlerReturn = self.handle(props)

                except Exception as error:
                    return self.catch(error)

                else:
                    return target(*args, **{**kwargs, **(handler_return or {})})

            return wrapper

        return decorator
