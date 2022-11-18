from typing import Type


class NameControllerNotDefinedError(Exception):
    def __init__(
        self,
        controller: Type
    ) -> None:
        super().__init__(
          f"Controller name not defined in {controller.__name__}"  
        )