from flask_socketio import Namespace
from abc import ABC


class Controller(Namespace, ABC):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def on_connect(self) -> None:
        pass

    def on_disconnect(self) -> None:
        pass
