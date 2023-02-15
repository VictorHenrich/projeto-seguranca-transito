from jwt import PyJWT
from typing import Sequence, TypeAlias, Any, Mapping, TypeVar, Type, Optional, Union


T = TypeVar("T")

JWTOptions: TypeAlias = Mapping[str, Any]

JWTPayload: TypeAlias = Union[JWTOptions, T]


class UtilsJWT:
    algorithm: Sequence[str] = ["HS256"]

    @classmethod
    def decode(
        cls,
        token: str,
        key: str,
        class_: Optional[Type[T]] = None,
        **options: JWTOptions
    ) -> JWTPayload:

        payload: JWTPayload = PyJWT().decode(token, key, list(cls.algorithm), **options)

        if class_:
            return class_(**payload)

        else:
            return payload

    @classmethod
    def encode(cls, payload: Mapping[str, Any], key: str, **options: JWTOptions) -> str:
        return PyJWT().encode(payload, key, list(cls.algorithm)[0], **options)
