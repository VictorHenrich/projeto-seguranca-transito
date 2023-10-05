from jwt import PyJWT
from typing import Collection, Any, Type, Optional

from utils.types import DictType


class JWTUtils:
    algorithm: Collection[str] = ["HS256"]

    @classmethod
    def decode(
        cls, token: str, key: str, class_: Optional[Type[Any]] = None, **options: Any
    ) -> Any:
        payload: DictType = PyJWT().decode(token, key, list(cls.algorithm), **options)

        if class_:
            return class_(**payload)

        else:
            return payload

    @classmethod
    def encode(cls, payload: DictType, key: str, **options: Any) -> str:
        return PyJWT().encode(dict(payload), key, list(cls.algorithm)[0], **options)
