
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Callable, Coroutine
import asyncio
from .database import Databases, Database
from .http import ServerHttp, ServerHttpBuilder
from .websocket import ServerSocket, ServerSocketBuilder
from .database.dialects import MySQL, Postgres, DialectDefaultBuilder


@dataclass
class Server:

    def __init__(
        self,
        http: ServerHttp,
        databases: Databases,
        websocket: Optional[ServerSocket]
    ) -> None:
        self.__http: ServerSocket = http
        self.__databases: Databases = databases
        self.__websocket: Optional[ServerSocket] = websocket
        self.__listeners: list[Callable[[None], None]] = []

    @property
    def databases(self) -> Databases:
        return self.__databases

    @property
    def http(self) -> ServerHttp:
        return self.__http

    @property
    def websocket(self) -> Optional[ServerSocket]:
        return self.__websocket

    def start(self, target: Callable[[None], None]) -> Callable[[None], None]:
        self.__listeners.append(target)

        return target

    def start_server(self) -> None:
        for target in self.__listeners:
            result: Any = target()

            if isinstance(result, Coroutine):
                asyncio.run(result)


class ServerFectory:
    __dialects: list[DialectDefaultBuilder] = [MySQL, Postgres]

    @classmethod
    def create(
        cls,
        app: Mapping[str, Any],
        databases: Mapping[str, Any],
        websocket: Optional[Mapping[str, Any]]
    ) -> Server:
        server_http: ServerHttp = \
            ServerHttpBuilder()\
                .set_host(app['host'])\
                .set_port(app['port'])\
                .set_debug(app['debug'])\
                .build()


        server_databases: Databases = Databases()

        for name, config in databases.items():
            dialect, = [
                d
                for d in cls.__dialects
                if d.name_base == config['dialect']
            ]

            database: Database = \
                dialect \
                    .set_host(config['host'])\
                    .set_port(config['port'])\
                    .set_credentials(config['user'], config['password'])\
                    .set_dbname(config['dbname'])\
                    .set_debug(config['debug'])\
                    .set_async(config['async'])\
                    .set_name(name)\
                    .build()

            server_databases.append_databases(database)

        server_websocket: Optional[ServerSocket] = None

        if websocket:
            server_websocket = \
                ServerSocketBuilder()\
                    .set_app(server_http)\
                    .set_host(websocket['host'])\
                    .set_port(websocket['port'])\
                    .set_debug(websocket['debug'])\
                    .build()


        return Server(
            server_http,
            server_databases,
            server_websocket
        )