from abc import ABC
from dataclasses import dataclass
from __future__ import annotations
from typing import Optional, Union
from ..database import Database

@dataclass
class Parameters:
    name: Optional[str]
    connection_url: str
    async_: bool
    debug: bool


@dataclass
class DialectDefaultBuilder(ABC):
    name: str
    host: str
    port: Union[str, int]
    dbname: str
    username: str
    password: str
    driver_default: str
    driver_async: str
    async_: bool = False
    debug: bool = False
    name_base: str = None

    def set_name(self, name: str) -> DialectDefaultBuilder:
        self.name = name

        return self

    def set_name_base(self, name_base: str) -> DialectDefaultBuilder:
        self.name_base = name_base

        return self

    def set_dbname(self, dbname: str) -> DialectDefaultBuilder:
        self.dbname = dbname

        return self

    def set_host(self, host: str) -> DialectDefaultBuilder:
        self.host = host

        return self

    def set_port(self, port: Union[str, int]) -> DialectDefaultBuilder:
        self.port = port

        return self

    def set_credentials(self, username: str, password: str) -> DialectDefaultBuilder:
        self.username = username
        self.password = password

        return self

    def set_driver_default(self, driver: str) -> DialectDefaultBuilder:
        self.driver_default = driver

        return self

    def set_driver_async(self, driver: str) -> DialectDefaultBuilder:
        self.driver_async = driver

        return self

    def set_async(self, async_: bool) -> DialectDefaultBuilder:
        self.async_ = async_

        return self

    def set_debug(self, debug: bool) -> DialectDefaultBuilder:
        self.debug = debug

        return

    def build(self) -> Database:
        driver: str = self.driver_default if not self.async_ else self.driver_async

        url: str = f"{self.name_base}+{driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"

        parameters: Parameters = Parameters(self.name, url, self.async_, self.debug)

        return Database(parameters)