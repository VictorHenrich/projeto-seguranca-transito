from typing import Any, Mapping, Optional, Callable, TypeAlias, TypeVar, Generic
from abc import ABC, abstractmethod
from flask import Response

from exceptions import MiddlewareErrorValue

T = TypeVar("T")
E = TypeVar("E", bound=Exception, contravariant=True)

HandlerReturn: TypeAlias = Optional[Mapping[str, Any]]
Target: TypeAlias = Callable[[Any], Response]
Wrapper: TypeAlias = Callable[[Any], Response]
Decorator: TypeAlias = Callable[[Any], Wrapper]


class HttpMiddleware(ABC, Generic[T]):
    @abstractmethod
    def handle(self, props: Optional[T]) -> HandlerReturn:
        ...

    def catch(self, exception: Exception) -> Response:
        raise exception

    def apply(self, props: Optional[T] = None) -> Decorator:
        def decorator(target: Target) -> Wrapper:
            def wrapper(*args: Any, **kwargs: Any) -> Response:
                try:
                    if type(props) is not T:
                        raise MiddlewareErrorValue()

                    handler_return: HandlerReturn = self.handle(props)

                except Exception as error:
                    return self.catch(error)

                else:
                    return target(*args, **{**kwargs, **(handler_return or {})})

            return wrapper

        return decorator
