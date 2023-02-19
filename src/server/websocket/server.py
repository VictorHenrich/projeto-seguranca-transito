from flask import Flask
from flask_socketio import SocketIO
from typing import Protocol, Type, Union, List, TypeAlias, Callable, Dict
from dataclasses import dataclass

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
    debug: bool = True


class ISocketClient(Protocol):
    id: StringOrNumber
    info: Dict


class SocketServer(SocketIO):
    def __init__(self, config: SocketServerConfig):
        self.__app: Flask = Flask(__name__)

        self.__config: SocketServerConfig = config

        self.__clients: List[ISocketClient] = []

        super().__init__(self.__app)

    @property
    def config(self) -> SocketServerConfig:
        return self.__config

    @property
    def clients(self) -> List[ISocketClient]:
        return self.__clients

    def run(self) -> None:
        super().run(
            self.__app,
            self.__config.host,
            self.__config.port,
            debug=self.__config.debug,
        )

    def add_client(self, client: ISocketClient) -> None:
        self.__clients.append(client)

    def get_client(self, id: StringOrNumber) -> ISocketClient:
        for client in self.__clients:
            if client.id == id:
                return client

    def add_controller(self, controller_name: str) -> DecoratorAddController:
        def wrapper(cls: TypeSocketController) -> TypeSocketController:
            self.on_namespace(cls(controller_name))

            return cls

        return wrapper
