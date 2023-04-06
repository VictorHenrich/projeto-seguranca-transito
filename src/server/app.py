from typing import Callable, Any, Dict, TypeAlias
from .http import HttpServer, HttpServerBuilder
from .websocket import SocketServer, SocketServerBuilder
from .database import Databases, DatabaseBuilder
from .cli import ManagerController


Target: TypeAlias = Callable[[None], None]
ParamDict: TypeAlias = Dict[str, Any]


class App:
    __http: HttpServer
    __databases: Databases
    __websocket: SocketServer
    __cli: ManagerController

    @classmethod
    def http(cls) -> HttpServer:
        return cls.__http

    @classmethod
    def databases(cls) -> Databases:
        return cls.__databases

    @classmethod
    def websocket(cls) -> SocketServer:
        return cls.__websocket

    @classmethod
    def cli(cls) -> ManagerController:
        return cls.__cli

    @classmethod
    def __create_http(cls, data: ParamDict) -> None:
        cls.__http = (
            HttpServerBuilder()
            .set_host(data["host"])
            .set_port(data["port"])
            .set_debug(data["debug"])
            .set_secret_key(data["secret_key"])
            .build()
        )

    @classmethod
    def __create_databases(cls, data: Dict[str, ParamDict]) -> None:
        databases: Databases = Databases()

        for base_name, base_props in data.items():
            databases.append_databases(
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

        cls.__databases = databases

    @classmethod
    def __create_websocket(cls, data: ParamDict) -> None:
        cls.__websocket = (
            SocketServerBuilder()
            .set_host(data["host"])
            .set_port(data["port"])
            .set_debug(data["debug"])
            .set_secret_key(data["secret_key"])
            .build()
        )

    @classmethod
    def __create_cli(cls, data: ParamDict) -> None:
        manager_controller: ManagerController = ManagerController(
            name=data["name"], description=data["description"], version=data["version"]
        )

        for manager_name in data["managers"]:
            manager_controller.create_task_manager(manager_name)

        cls.__cli = manager_controller

    @classmethod
    def init_server(
        cls, http: ParamDict, databases: ParamDict, websocket: ParamDict, cli: ParamDict
    ) -> None:
        cls.__create_http(http)
        cls.__create_databases(databases)
        cls.__create_websocket(websocket)
        cls.__create_cli(cli)

    @classmethod
    def start(cls) -> None:
        cls.__cli.run()
