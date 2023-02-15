from flask_socketio import Namespace
from abc import ABC
from typing import Optional


class Controller(ABC, Namespace):
    name: str = ""

    def __init__(self, name: Optional[str] = None) -> None:
        namespace: str = self.__class__.name or name

        super().__init__(namespace)

    def on_connect(self) -> None:
        pass

    def on_disconnect(self) -> None:
        pass
