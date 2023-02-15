from typing import Type, Sequence


class UtilsExcept:
    @classmethod
    def fired(
        cls, obj: BaseException, *exceptions: Sequence[Type[BaseException]]
    ) -> bool:
        return type(obj) in exceptions
