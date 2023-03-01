from abc import ABC, abstractclassmethod
from flask import Response
from typing import (
    Any,
    Dict,
    Optional,
    Callable,
    TypeAlias,
    Tuple
)


Args: TypeAlias = Tuple[Any, ...]
Kwargs: TypeAlias = Dict[str, Any]
Handler: TypeAlias = Optional[Dict[str, Any]]
Target: TypeAlias = Callable[[Any], Response]
Wrapper: TypeAlias = Callable[[Any], Response]
Decorator: TypeAlias = Callable[[Target], Wrapper]


class Middleware(ABC):
    @abstractclassmethod
    def handle(
        cls, *args: Args, **kwargs: Kwargs
    ) -> Handler:
        pass

    @classmethod
    def catch(cls, exception: Exception) -> Response:
        raise exception

    @classmethod
    def apply(cls, *args: Args, **kwargs: Kwargs) -> Decorator:
        def decorator(target: Target) -> Wrapper:
            def wrapper(*args_w: Args, **kwargs_w: Kwargs) -> Response:
                try:
                    handler_return: Handler = cls.handle(*args, **kwargs)

                except Exception as error:
                    return cls.catch(error)

                else:
                    return target(*args_w, **{**kwargs_w, **(handler_return or {})})

            return wrapper

        return decorator
