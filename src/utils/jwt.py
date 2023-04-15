from jwt import PyJWT
from typing import Sequence, TypeAlias, Any, Dict, Type, Optional


DictMapping: TypeAlias = Dict[str, Any]


class UtilsJWT:
    algorithm: Sequence[str] = ["HS256"]

    @classmethod
    def decode(
        cls, token: str, key: str, class_: Optional[Type[Any]] = None, **options: Any
    ) -> Any:
        payload: DictMapping = PyJWT().decode(
            token, key, list(cls.algorithm), **options
        )

        if class_:
            return class_(**payload)

        else:
            return payload

    @classmethod
    def encode(cls, payload: DictMapping, key: str, **options: Any) -> str:
        return PyJWT().encode(payload, key, list(cls.algorithm)[0], **options)