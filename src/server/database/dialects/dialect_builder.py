from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
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
    dialect: str = ""
    name: str = None
    host: Optional[str] = None
    port: Optional[Union[str, int]] = None
    dbname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    driver_default: Optional[str] = None
    driver_async: Optional[str] = None
    async_: bool = False
    debug: bool = False

    def set_name(self, name: str) -> DialectDefaultBuilder:
        self.name = name

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

        return self

    def build(self) -> Database:
        driver: str = self.driver_default if not self.async_ else self.driver_async

        url: str = f"{self.dialect}+{driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"

        parameters: Parameters = Parameters(self.name, url, self.async_, self.debug)

        return Database(parameters)
