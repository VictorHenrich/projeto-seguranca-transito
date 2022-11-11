from typing import Any, Mapping, Protocol, Union
from flask import Flask
from flask_restful import Api

from .controller import Controller




class ConfigServer(Protocol):
    host: str
    port: Union[str, int]
    secret_key: str
    debug: bool = True


class ServerHttp(Api):
    def __init__(
        self,
        config: ConfigServer,
        **options: Mapping[str, Any]
    ):
        self.__configs: ConfigServer = config

        self.__application: Flask = Flask(__name__)

        self.__application.secret_key = self.__configs.secret_key

        super().__init__(self.__application, **options)

    @property
    def configs(self) -> ConfigServer:
        return self.__configs

    @property
    def application(self) -> Flask:
        return self.__application

    def start_app(self) -> None:
        self.__application.run(**self.__configs.__dict__)

    def add_route(self, controller: Controller, *urls: str, **kwargs: Mapping[str, Any]):
        return self.add_resource(controller, *urls, **kwargs)