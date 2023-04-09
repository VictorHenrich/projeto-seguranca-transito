from typing import Any, Dict, Optional, Callable, TypeAlias, TypeVar, Generic
from abc import ABC, abstractmethod


T = TypeVar("T")

HandlerReturn: TypeAlias = Optional[Dict[str, Any]]
Wrapper: TypeAlias = Callable[[Any], Any]
Target: TypeAlias = Callable[[Any], Any]
Decorator: TypeAlias = Callable[[Target], Wrapper]


class SocketMiddleware(ABC, Generic[T]):
    @abstractmethod
    def handle(self, props: T) -> HandlerReturn:
        ...

    def catch(self, exception: Exception) -> None:
        raise exception

    def apply(self, props: T) -> Decorator:
        def decorator(target: Target) -> Wrapper:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    handler_return: HandlerReturn = self.handle(props)

                except Exception as error:
                    return self.catch(error)

                else:
                    return target(*args, **{**kwargs, **(handler_return or {})})

            return wrapper

        return decorator
