from flask_socketio import Namespace
from abc import ABC

from .exceptions import NameControllerNotDefinedError



class Controller(Namespace, ABC):
    name: str

    def __init__(self) -> None:
        controller_name: str = self.__class__.name

        if not controller_name:
            raise NameControllerNotDefinedError(self.__class__)

        super().__init__(controller_name)

    def on_connect(self) -> None:
        pass

    def on_disconnect(self) -> None:
        pass