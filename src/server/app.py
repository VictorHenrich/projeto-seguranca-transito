from typing import (
    Callable,
    Coroutine,
    Union,
    Any,
    Mapping,
    Sequence,
    TypeAlias,
)
from multiprocessing import Process
from threading import Thread
from queue import Queue
import asyncio
from server.http import HttpServer, HttpServerConfig
from server.websocket import SocketServer, SocketServerConfig
from server.database import Databases
from server.database.dialects import MySQL, Postgres, DialectDefaultBuilder


Target: TypeAlias = Callable[[None], None]
ParamDict: TypeAlias = Mapping[str, Any]


class App:
    def __init__(
        self,
        http: HttpServer,
        databases: Databases,
        websocket: SocketServer = None,
    ) -> None:
        self.__http: HttpServer = http
        self.__databases: Databases = databases
        self.__websocket: SocketServer = websocket

        self.__listeners: Sequence[Process] = []

    @property
    def http(self) -> HttpServer:
        return self.__http

    @property
    def databases(self) -> Databases:
        return self.__databases

    @property
    def websocket(self) -> SocketServer:
        return self.__websocket

    def initialize(self, t: Target) -> Target:
        process: Process = Process(target=t)

        self.__listeners.append(process)

        return t

    def start(self) -> None:
        [process.start() for process in self.__listeners]
        [process.join() for process in self.__listeners]


class AppFactory:

    __bases: Sequence[DialectDefaultBuilder] = [MySQL(), Postgres()]

    @classmethod
    def __handle_http(cls, data: ParamDict) -> HttpServer:
        config: HttpServerConfig = HttpServerConfig(
            host=data["host"],
            port=data["port"],
            debug=data["debug"],
            secret_key=data["secret_key"],
        )

        return HttpServer(config)

    @classmethod
    def __handle_databases(cls, data: Mapping[str, ParamDict]) -> Databases:
        databases: Databases = Databases()

        for base_name, base_props in data.items():
            base: DialectDefaultBuilder = DialectDefaultBuilder()

            localized_base: list[DialectDefaultBuilder] = [
                b
                for b in cls.__bases
                if b.dialect.upper() == base_props["dialect"].upper()
            ]

            if localized_base:
                base = localized_base[0]

            base.set_name(base_name).set_host(base_props["host"]).set_port(
                base_props["port"]
            ).set_dbname(base_props["dbname"]).set_credentials(
                base_props["username"], base_props["password"]
            )

            if base_props.get("debug"):
                base.set_debug(base_props["debug"])

            if base_props.get("async"):
                base.set_async(base_props["async"])

            databases.append_databases(base.build())

        return databases

    @classmethod
    def __handle_websocket(cls, data: ParamDict) -> SocketServer:
        config: SocketServerConfig = SocketServerConfig(
            host=data["host"],
            port=data["port"],
            secret_key=data["secret_key"],
            debug=data["debug"],
        )

        app_socket: SocketServer = SocketServer(config)

        return app_socket

    @classmethod
    def create(
        cls,
        http: ParamDict,
        databases: ParamDict,
        websocket: ParamDict,
    ) -> App:
        instance_http: HttpServer = cls.__handle_http(http)
        instance_databases: Databases = cls.__handle_databases(databases)
        instance_websocket: SocketServer = cls.__handle_websocket(websocket)

        return App(
            http=instance_http,
            databases=instance_databases,
            websocket=instance_websocket,
        )
