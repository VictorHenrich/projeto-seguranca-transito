from typing import Any, Mapping, Union
from dataclasses import dataclass
from flask import Flask
from flask_restful import Api

from .controller import Controller



@dataclass
class HttpServerConfig:
    host: str
    port: Union[str, int]
    debug: bool = True



class HttpServer(Api):
    def __init__(self, config: HttpServerConfig):
        self.__configs: HttpServerConfig = config

        self.__application: Flask = Flask(__name__)

        super().__init__(self.__application)

    @property
    def configs(self) -> HttpServerConfig:
        return self.__configs

    @property
    def application(self) -> Flask:
        return self.__application

    def start_app(self) -> None:
        self.__application.run(**self.__configs.__dict__)

    def add_resource(self, controller: Controller, *urls: str, **kwargs: Mapping[str, Any]):
        return super().add_resource(controller, *urls, **kwargs)