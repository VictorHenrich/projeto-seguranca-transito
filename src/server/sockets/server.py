from flask_socketio import SocketIO
from flask import Flask
from typing import Optional, Union
from dataclasses import dataclass

from server.http import HttpServer


@dataclass
class SocketServerConfig:
    host: Optional[str] = None
    port: Optional[Union[str, int]] = None
    debug: bool = True


class SocketServer(SocketIO):
    def __init__(self, http: Optional[HttpServer], config: SocketServerConfig) -> None:
        self.__configs: SocketServerConfig = config

        self.__application: Flask = http.application if http else Flask(__name__)

        super().__init__(self.__application)

    @property
    def configs(self) -> SocketServerConfig:
        return self.__configs

    @property
    def application(self) -> Flask:
        return self.__application

    def start_app(self) -> None:
        self.run(self.__application, **self.__configs.__dict__)

    def add_resource(self) -> None:
        pass
