from typing import Type, Sequence


class UtilsExcept:
    @classmethod
    def fired(cls, obj: BaseException, *exceptions: Type[Exception]) -> bool:
        return type(obj) in exceptions
