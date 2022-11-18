from typing import (
    Optional, 
    Callable, 
    Coroutine, 
    Union, 
    Any, 
    Mapping,
    Sequence
)
import asyncio
from server.http import HttpServer, HttpServerConfig
from server.sockets import SocketServer, SocketServerConfig
from server.database import Databases
from server.database.dialects import (
    MySQL,
    Postgres,
    DialectDefaultBuilder
)




class App:
    def __init__(
        self,
        http: HttpServer,
        databases: Databases,
        websocket: Optional[SocketServer] = None
    ) -> None:
        self.__http: HttpServer = http
        self.__databases: Databases = databases
        self.__websocket: Optional[SocketServer] = websocket

        self.__listeners: list[Callable[[None], None]] = []

    @property
    def http(self) -> HttpServer:
        return self.__http

    @property
    def databases(self) -> Databases:
        return self.__databases

    @property
    def websocket(self) -> Optional[SocketServer]:
        return self.__websocket

    def initialize(self, target: Callable[[None], None]) -> Callable[[None], None]:
        self.__listeners.append(target)

        return target

    def start(self) -> None:
        for target in self.__listeners:
            result: Union[Coroutine, Any] = target()

            if isinstance(result, Coroutine):
                asyncio.run(result)




class AppFactory:

    __bases: Sequence[DialectDefaultBuilder] = [
        MySQL(),
        Postgres()
    ]

    @classmethod
    def __handle_http(cls, data: Mapping[str, Any]) -> HttpServer:
        config: HttpServerConfig = HttpServerConfig(
            host=data['host'],
            port=data['port'],
            debug=data['debug'],
            secret_key=data['secret_key']
        )

        return HttpServer(config)

    @classmethod
    def __handle_databases(cls, data: Mapping[str, Mapping]) -> Databases:
        databases: Databases = Databases()

        for base_name, base_props in data.items():
            base: DialectDefaultBuilder = DialectDefaultBuilder()

            localized_base: list[DialectDefaultBuilder] = [
                b
                for b in cls.__bases
                if b.dialect.upper() == base_props['dialect'].upper()
            ]

            if localized_base:
                base = localized_base[0]

            base\
                .set_name(base_name)\
                .set_host(base_props['host'])\
                .set_port(base_props['port'])\
                .set_dbname(base_props['dbname'])\
                .set_credentials(base_props['username'], base_props['password'])

            if base_props.get('debug'):
                base.set_debug(base_props['debug'])

            if base_props.get('async'):
                base.set_async(base_props['async'])

            databases.append_databases(base.build())

        return databases

    @classmethod
    def __handle_websocket(cls, http: SocketServer, data: Optional[Mapping]) -> Optional[SocketServer]:
        if not data:
            return None

        config: SocketServerConfig = SocketServerConfig(
            host=data['host'],
            port=data['port'],
            debug=data['debug']
        )

        app_socket: SocketServer = SocketServer(http, config)

        return app_socket

    @classmethod
    def create(
        cls,
        http: Mapping[str, Any],
        databases: Mapping[str, Any],
        websocket: Optional[Mapping[str, Any]] = None
    ) -> App:
        instance_http: HttpServer = cls.__handle_http(http)
        instance_databases: Databases = cls.__handle_databases(databases)
        instance_websocket: Optional[SocketServer] = cls.__handle_websocket(instance_http, websocket)

        return App(
            http=instance_http,
            databases=instance_databases,
            websocket=instance_websocket
        )

