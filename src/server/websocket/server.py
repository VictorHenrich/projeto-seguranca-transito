from typing import Protocol, Type, Union, Any, TypeAlias, Callable, Dict, List

from flask import Flask, request, Request
from flask_socketio import SocketIO
from socketio import Client

from .controller import Controller


TypeSocketController: TypeAlias = Type[Controller]
DecoratorAddController: TypeAlias = Callable[
    [TypeSocketController], TypeSocketController
]
StringOrNumber: TypeAlias = Union[str, int]


class SocketServerConfig(Protocol):
    host: str
    port: StringOrNumber
    secret_key: str
    debug: bool


class SocketServer(SocketIO):
    def __init__(self, config: SocketServerConfig):
        app: Flask = Flask(__name__)

        app.secret_key = config.secret_key

        self.__app: Flask = app

        self.__config: SocketServerConfig = config

        self.__global_request: Request = request

        self.__controllers: Dict[str, Controller] = {}

        super().__init__(self.__app, cors_allowed_origins="*")

    @property
    def global_request(self) -> Request:
        return self.__global_request

    @property
    def config(self) -> SocketServerConfig:
        return self.__config

    def run(self) -> None:
        super().run(
            self.__app,
            self.__config.host,
            self.__config.port,
            debug=self.__config.debug,
        )

    def add_controller(self, controller_name: str) -> DecoratorAddController:
        def wrapper(cls: TypeSocketController) -> TypeSocketController:
            controller: Controller = cls(controller_name)

            self.on_namespace(controller)

            self.__controllers[controller_name] = controller

            return cls

        return wrapper

    def emit_controller(self, namespace: str, event: str, data: Any) -> None:
        controllers_names: List[str] = [
            controller_name for controller_name in self.__controllers.keys()
        ]

        url: str = f"http://{self.__config.host}:{self.__config.port}"

        client: Client = Client(logger=True)

        client.connect(url, namespaces=controllers_names)

        client.emit(event, data, namespace=namespace)

        client.disconnect()
