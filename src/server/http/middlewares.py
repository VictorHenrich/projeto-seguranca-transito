from typing import Any, Dict, Optional, Callable, TypeAlias, TypeVar, Generic
from abc import ABC, abstractmethod
from flask import Response


T = TypeVar("T")
E = TypeVar("E", bound=Exception, contravariant=True)

HandlerReturn: TypeAlias = Optional[Dict[str, Any]]
Target: TypeAlias = Callable[[Any], Response]
Wrapper: TypeAlias = Callable[[Any], Response]
Decorator: TypeAlias = Callable[[Any], Wrapper]


class HttpMiddleware(ABC, Generic[T]):
    @abstractmethod
    def handle(self, props: T) -> HandlerReturn:
        ...

    def catch(self, exception: Exception) -> Response:
        raise exception

    def apply(self, props: T) -> Decorator:
        def decorator(target: Target) -> Wrapper:
            def wrapper(*args: Any, **kwargs: Any) -> Response:
                try:
                    handler_return: HandlerReturn = self.handle(props)

                except Exception as error:
                    return self.catch(error)

                else:
                    return target(*args, **{**kwargs, **(handler_return or {})})

            return wrapper

        return decorator
