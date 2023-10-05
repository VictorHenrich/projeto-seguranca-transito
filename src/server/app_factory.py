from typing import Callable, Mapping, TypeAlias, Optional
from pika import ConnectionParameters
import logging

from .http import HttpServer, HttpServerConfig
from .websocket import SocketServer, SocketServerConfig
from .database import Databases, DatabaseBuilder
from .cli import CLI
from .amqp import AMQPServer, ConnectionBuilder
from utils.types import DictType


Target: TypeAlias = Callable[[None], None]

logging.basicConfig(level=logging.INFO)


class AppFactory:
    @classmethod
    def __create_amqp(cls, data: Optional[DictType]) -> None:
        if data:
            amqp_connection: ConnectionParameters = (
                ConnectionBuilder()
                .set_host(data["host"])
                .set_port(data["port"])
                .set_credentials(data["username"], data["password"])
                .build()
            )

            AMQPServer.set_default_connection(amqp_connection)

    @classmethod
    def __create_http(cls, data: Optional[DictType]) -> None:
        if data:
            http_config: HttpServerConfig = HttpServerConfig(
                data["host"], data["port"], data["secret_key"], data["debug"]
            )

            HttpServer.set_config(http_config)

    @classmethod
    def __create_databases(cls, data: Optional[Mapping[str, DictType]]) -> None:
        if data:
            for base_name, base_props in data.items():
                Databases.append_databases(
                    DatabaseBuilder()
                    .set_name(base_name)
                    .set_dialect(base_props["dialect"])
                    .set_host(base_props["host"])
                    .set_port(base_props["port"])
                    .set_dbname(base_props["dbname"])
                    .set_driver(base_props["driver"])
                    .set_credentials(base_props["username"], base_props["password"])
                    .set_debug(base_props.get("debug") or False)
                    .build()
                )

    @classmethod
    def __create_websocket(cls, data: Optional[DictType]) -> None:
        if data:
            socket_config: SocketServerConfig = SocketServerConfig(
                data["host"], data["port"], data["secret_key"], data["debug"]
            )

            SocketServer.set_config(socket_config)

    @classmethod
    def __create_cli(cls, data: Optional[DictType]) -> None:
        if data:
            CLI.set_config(
                data["name"], data["description"], data["version"], *data["managers"]
            )

    @classmethod
    def init_server(
        cls,
        http: Optional[DictType] = None,
        databases: Optional[DictType] = None,
        websocket: Optional[DictType] = None,
        cli: Optional[DictType] = None,
        amqp: Optional[DictType] = None,
    ) -> None:
        cls.__create_http(http)
        cls.__create_databases(databases)
        cls.__create_websocket(websocket)
        cls.__create_cli(cli)
        cls.__create_amqp(amqp)
