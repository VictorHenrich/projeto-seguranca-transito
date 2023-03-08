from abc import ABC, abstractclassmethod
from typing import Any, Dict, Optional, Callable, TypeAlias, Sequence


Kwargs: TypeAlias = Dict[str, Any]
Args: TypeAlias = Sequence[Any]
Wrapper: TypeAlias = Callable[[Any], Any]
Target: TypeAlias = Callable[[Any], Any]
Decorator: TypeAlias = Callable[[Callable[[Any], Any]], Wrapper]


class Middleware(ABC):
    @abstractclassmethod
    def handle(
        cls, *args: Optional[Args], **kwargs: Optional[Kwargs]
    ) -> Optional[Kwargs]:
        ...

    @classmethod
    def catch(cls, exception: Exception) -> None:
        raise exception

    @classmethod
    def apply(cls, *args: Optional[Args], **kwargs: Optional[Kwargs]) -> Decorator:
        def decorator(
            target: Target,
        ) -> Wrapper:
            def wrapper(*args_w: Optional[Args], **kwargs_w: Optional[Kwargs]) -> Any:
                try:
                    handler_return: Optional[Optional[Kwargs]] = cls.handle(
                        *args, **kwargs
                    )

                except Exception as error:
                    return cls.catch(error)

                else:
                    return target(*args_w, **{**kwargs_w, **(handler_return or {})})

            return wrapper

        return decorator
