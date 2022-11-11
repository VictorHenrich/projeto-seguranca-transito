from abc import ABC, abstractclassmethod
from flask import Response
from typing import (
    Any, 
    Mapping, 
    Optional, 
    Sequence, 
    Callable,
    TypeAlias,
    TypeVar,
    Generic
)


MiddlewareArgs: TypeAlias = Sequence[Any]

MiddlewareKwargs: TypeAlias = Mapping[str, Any]

MiddlewareHandled: TypeAlias = Optional[Mapping[str, Any]]

MiddlewareTarget: TypeAlias = Callable[[Any], Response]



class Middleware(ABC):
    @abstractclassmethod
    def handle(cls, *args: MiddlewareArgs, **kwargs: MiddlewareKwargs) -> MiddlewareHandled:
        pass

    @classmethod
    def catch(cls, exception: Exception) -> Optional[Response]:
        raise exception

    @classmethod
    def apply(cls, *args: MiddlewareArgs, **kwargs: MiddlewareKwargs) -> Callable:

        """
            Isto é um decorator responsável por aplicar alguma funcionalidade intermediaria ao metodo 
            http criada a partir da classe Middleware
        """

        def wrapper(target: MiddlewareTarget) -> MiddlewareTarget:
            def w(*args_w: MiddlewareArgs, **kwargs_w: MiddlewareKwargs) -> Response:
                try:
                    handler_return: MiddlewareHandled = cls.handle(*args, **kwargs)

                except Exception as error:
                    return cls.catch(error)

                else:
                    return target(*args_w, {**kwargs_w, **(handler_return or {})})

            return w

        return wrapper