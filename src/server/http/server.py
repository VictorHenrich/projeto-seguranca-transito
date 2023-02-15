from typing import Any, Mapping, Union
from dataclasses import dataclass
from flask import Flask
from flask_restful import Api

from .controller import Controller


@dataclass
class HttpServerConfig:
    host: str
    port: Union[str, int]
    secret_key: str
    debug: bool = True


class HttpServer(Api):
    def __init__(self, config: HttpServerConfig):
        self.__configs: HttpServerConfig = config

        self.__application: Flask = Flask(__name__)

        self.__application.secret_key = self.__configs.secret_key

        super().__init__(self.__application)

    @property
    def configs(self) -> HttpServerConfig:
        return self.__configs

    @property
    def application(self) -> Flask:
        return self.__application

    def start_app(self) -> None:
        self.__application.run(
            host=self.__configs.host,
            port=self.__configs.port,
            debug=self.__configs.debug,
        )

    def add_route(
        self, controller: Controller, *urls: str, **kwargs: Mapping[str, Any]
    ):
        return self.add_resource(controller, *urls, **kwargs)
