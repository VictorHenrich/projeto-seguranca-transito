from typing import (
    Any,
    Dict,
    Union,
    Type,
    Callable,
    TypeAlias,
    Protocol,
    Sequence,
    Optional,
)
from flask import Flask, Request, request
from flask_cors import CORS
from flask_restful import Api

from .controller import Controller


Kwargs: TypeAlias = Dict[str, Any]


class HttpServerConfig(Protocol):
    host: str
    port: Union[str, int]
    secret_key: str
    debug: bool


class HttpServer(Api):
    def __init__(self, config: HttpServerConfig):
        self.__configs: HttpServerConfig = config

        self.__application: Flask = Flask(__name__)

        self.__cors: CORS = CORS(self.__application)

        self.__global_request: Request = request

        self.__application.secret_key = self.__configs.secret_key

        super().__init__(self.__application)

    @property
    def configs(self) -> HttpServerConfig:
        return self.__configs

    @property
    def application(self) -> Flask:
        return self.__application

    @property
    def cors(self) -> CORS:
        return self.__cors

    @property
    def global_request(self) -> Request:
        return self.__global_request

    def run(self) -> None:
        self.__application.run(
            host=self.__configs.host,
            port=int(self.__configs.port),
            debug=self.__configs.debug,
        )

    def add_controller(
        self, *urls: Sequence[str], **kwargs: Kwargs
    ) -> Callable[[Type[Controller]], Type[Controller]]:
        def wrapper(cls: Type[Controller]) -> Type[Controller]:
            self.add_resource(cls, *urls, **kwargs)

            return cls

        return wrapper
