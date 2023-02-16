from typing import Optional, Callable, Coroutine, Union, Any, Mapping, Sequence, TypeAlias
import asyncio
from threading import Thread
from server.http import HttpServer, HttpServerConfig
from server.sockets import SocketServer, SocketServerConfig
from server.database import Databases
from server.database.dialects import MySQL, Postgres, DialectDefaultBuilder



Target: TypeAlias = Callable[[None], None]
WebSocket: TypeAlias = Optional[SocketServer]
ParamDict: TypeAlias = Mapping[str, Any]


class App:
    def __init__(
        self,
        http: HttpServer,
        databases: Databases,
        websocket: WebSocket = None,
    ) -> None:
        self.__http: HttpServer = http
        self.__databases: Databases = databases
        self.__websocket: WebSocket = websocket

        self.__listeners: list[Target] = []

    @property
    def http(self) -> HttpServer:
        return self.__http

    @property
    def databases(self) -> Databases:
        return self.__databases

    @property
    def websocket(self) -> WebSocket:
        return self.__websocket

    def initialize(self, target: Target) -> Target:
        self.__listeners.append(target)

        return target

    def __handle_target(self, target: Target) -> None:
        result: Union[Coroutine, Any] = target()

        if isinstance(result, Coroutine):
            asyncio.run(result)

    def start(self) -> None:
        for target in self.__listeners:
            self.__handle_target(target)


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
    def __handle_websocket(
        cls, http: SocketServer, data: Optional[ParamDict]
    ) -> WebSocket:
        if not data:
            return None

        config: SocketServerConfig = SocketServerConfig(
            host=data["host"], port=data["port"], debug=data["debug"]
        )

        app_socket: SocketServer = SocketServer(http, config)

        return app_socket

    @classmethod
    def create(
        cls,
        http: ParamDict,
        databases: ParamDict,
        websocket: Optional[ParamDict] = None,
    ) -> App:
        instance_http: HttpServer = cls.__handle_http(http)
        instance_databases: Databases = cls.__handle_databases(databases)
        instance_websocket: WebSocket = cls.__handle_websocket(
            instance_http, websocket
        )

        return App(
            http=instance_http,
            databases=instance_databases,
            websocket=instance_websocket,
        )
