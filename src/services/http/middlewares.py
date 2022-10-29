from abc import ABC, abstractclassmethod
from typing import Any, Mapping, Optional, Sequence, Callable
from flask import Response



class Middleware(ABC):
    @abstractclassmethod
    def handle(cls, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        pass

    @classmethod
    def catch(cls, exception: Exception) -> Optional[Response]:
        raise exception

    @classmethod
    def apply(cls, *args: Sequence[Any], **kwargs: Mapping[str, Any]):

        """
            Isto é um decorator responsável por aplicar alguma funcionalidade intermediaria ao metodo 
            http criada a partir da classe Middleware
        """

        def wrapper(target: Callable) -> Callable[[Sequence[Any], Mapping[str, Any]]]:
            def w(*args_w: Sequence[Any], **kwargs_w: Mapping[str, Any]) -> Response:
                try:
                    handler_return: Optional[Mapping[str, Any]] = cls.handle(*args, **kwargs)

                except Exception as error:
                    return cls.catch(error)

                else:
                    return target(*args_w, {**kwargs_w, **(handler_return or {})})

            return w

        return wrapper