from typing import List, Type, Union, TypeAlias, Callable, Mapping
from dataclasses import dataclass
from flask import Flask, request, Request
from flask_socketio import SocketIO

from .controller import Controller


TypeSocketController: TypeAlias = Type[Controller]
DecoratorAddController: TypeAlias = Callable[
    [TypeSocketController], TypeSocketController
]
StringOrNumber: TypeAlias = Union[str, int]


@dataclass
class SocketServerConfig:
    host: str
    port: StringOrNumber
    secret_key: str
    debug: bool


class SocketServer(SocketIO):
    __app: Flask = Flask(__name__)

    __instance: SocketIO = SocketIO(Flask(__name__), cors_allowed_origins="*")

    __config: SocketServerConfig = SocketServerConfig(
        host="localhost", port=7000, secret_key="", debug=True
    )

    __global_request: Request = request

    __controllers: List[Controller] = []

    @classmethod
    @property
    def global_request(cls) -> Request:
        return cls.__global_request

    @classmethod
    @property
    def config(cls) -> SocketServerConfig:
        return cls.__config

    @classmethod
    def set_config(cls, config: SocketServerConfig) -> None:
        cls.__config = config

    @classmethod
    def get_controller(cls, name: str) -> Controller:
        (controller,) = [
            controller
            for controller in cls.__controllers
            if controller.namespace == name.upper()
        ]

        return controller

    @classmethod
    def run(cls) -> None:
        cls.__instance.run(
            cls.__app,
            cls.__config.host,
            cls.__config.port,
            debug=cls.__config.debug,
        )

    @classmethod
    def add_controller(cls, controller_name: str) -> DecoratorAddController:
        def wrapper(c: TypeSocketController) -> TypeSocketController:
            controller: Controller = c(controller_name)

            cls.__instance.on_namespace(controller)

            cls.__controllers.append(controller)

            return c

        return wrapper
