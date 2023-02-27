from jwt import PyJWT
from typing import Sequence, TypeAlias, Any, Dict, TypeVar, Type, Optional, Union


DictMapping: TypeAlias = Dict[str, Any]

T = TypeVar("T", covariant=True)


class UtilsJWT:
    algorithm: Sequence[str] = ["HS256"]

    @classmethod
    def decode(
        cls,
        token: str,
        key: str,
        class_: Optional[Type[T]] = None,
        **options: DictMapping
    ) -> Union[T, DictMapping]:

        payload: DictMapping = PyJWT().decode(token, key, list(cls.algorithm), **options)

        if class_:
            return class_(**payload)

        else:
            return payload

    @classmethod
    def encode(cls, payload: DictMapping, key: str, **options: DictMapping) -> str:
        return PyJWT().encode(payload, key, list(cls.algorithm)[0], **options)
