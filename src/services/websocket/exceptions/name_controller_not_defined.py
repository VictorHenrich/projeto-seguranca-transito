from typing import Type
from ..controller import Controller


class NameControllerNotDefinedError(Exception):
    def __init__(
        self,
        controller: Type[Controller]
    ) -> None:
        super().__init__(
          f"Controller name not defined in {controller.__name__}"  
        )