from typing import Callable, Any, Dict, Sequence, TypeAlias
from .http import HttpServer, HttpServerBuilder
from .websocket import SocketServer, SocketServerBuilder
from .database import Databases
from .database.dialects import MySQL, Postgres, DialectDefaultBuilder
from .cli import ManagerController


Target: TypeAlias = Callable[[None], None]
ParamDict: TypeAlias = Dict[str, Any]


class App:
    def __init__(
        self,
        http: HttpServer,
        databases: Databases,
        websocket: SocketServer,
        cli: ManagerController,
    ) -> None:
        self.__http: HttpServer = http
        self.__databases: Databases = databases
        self.__websocket: SocketServer = websocket
        self.__cli: ManagerController = cli

    @property
    def http(self) -> HttpServer:
        return self.__http

    @property
    def databases(self) -> Databases:
        return self.__databases

    @property
    def websocket(self) -> SocketServer:
        return self.__websocket

    @property
    def cli(self) -> ManagerController:
        return self.__cli

    def start(self) -> None:
        self.__cli.run()


class AppFactory:

    __bases: Sequence[DialectDefaultBuilder] = [MySQL(), Postgres()]

    @classmethod
    def __handle_http(cls, data: ParamDict) -> HttpServer:
        return (
            HttpServerBuilder()
            .set_host(data["host"])
            .set_port(data["port"])
            .set_debug(data["debug"])
            .set_secret_key(data["secret_key"])
            .build()
        )

    @classmethod
    def __handle_databases(cls, data: Dict[str, ParamDict]) -> Databases:
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
        return (
            SocketServerBuilder()
            .set_host(data["host"])
            .set_port(data["port"])
            .set_debug(data["debug"])
            .set_secret_key(data["secret_key"])
            .build()
        )

    @classmethod
    def __handle_cli(cls, data: ParamDict) -> ManagerController:
        manager_controller: ManagerController = ManagerController(
            name=data["name"], description=data["description"], version=data["version"]
        )

        for manager_name in data["managers"]:
            manager_controller.create_task_manager(manager_name)

        return manager_controller

    @classmethod
    def create(
        cls, http: ParamDict, databases: ParamDict, websocket: ParamDict, cli: ParamDict
    ) -> App:
        instance_http: HttpServer = cls.__handle_http(http)
        instance_databases: Databases = cls.__handle_databases(databases)
        instance_websocket: SocketServer = cls.__handle_websocket(websocket)
        instance_manager_controller: ManagerController = cls.__handle_cli(cli)

        return App(
            http=instance_http,
            databases=instance_databases,
            websocket=instance_websocket,
            cli=instance_manager_controller,
        )
