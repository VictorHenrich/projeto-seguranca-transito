from abc import ABC, abstractclassmethod
from typing import Any, Dict, Optional, Callable, TypeAlias, Tuple


Kwargs: TypeAlias = Dict[str, Any]
Args: TypeAlias = Tuple[Any, ...]
Wrapper: TypeAlias = Callable[[Any], None]
Target: TypeAlias = Callable[[Any], None]
Decorator: TypeAlias = Callable[[Callable[[Any], Any]], Wrapper]


class Middleware(ABC):
    @abstractclassmethod
    def handle(cls, *args: Args, **kwargs: Kwargs) -> Optional[Kwargs]:
        ...

    @classmethod
    def catch(cls, exception: Exception) -> None:
        raise exception

    @classmethod
    def apply(cls, *args: Args, **kwargs: Kwargs) -> Decorator:
        def decorator(
            target: Target,
        ) -> Wrapper:
            def wrapper(*args_w: Args, **kwargs_w: Kwargs) -> None:
                try:
                    handler_return: Optional[Kwargs] = cls.handle(*args, **kwargs)

                except Exception as error:
                    cls.catch(error)

                else:
                    target(*args_w, **{**kwargs_w, **(handler_return or {})})

            return wrapper

        return decorator
