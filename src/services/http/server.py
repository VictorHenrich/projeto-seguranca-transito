from ctypes import Union
from typing import Any, Mapping, Protocol
from flask import Flask
from flask_restful import Api

from .controller import Controller




class ConfigServer(Protocol):
    host: str
    port: Union[str, int]
    debug: bool = True


class ServerHttp(Api):
    def __init__(
        self,
        host: str,
        port: Union[int, str],
        debug: bool = True
    ):
        self.__configs: ConfigServer = ConfigServer(host, port, debug)

        self.__application: Flask = Flask(__name__)

        super().__init__(self.__application)

    @property
    def configs(self) -> ConfigServer:
        return self.__configs

    @property
    def application(self) -> Flask:
        return self.__application

    def start_app(self) -> None:
        self.__application.run(**self.__configs.__dict__)

    def add_resource(self, controller: Controller, *urls: str, **kwargs: Mapping[str, Any]):
        return super().add_resource(controller, *urls, **kwargs)