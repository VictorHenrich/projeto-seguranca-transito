from __future__ import annotations
from typing import Union, TypeAlias
from dataclasses import dataclass

from .server import HttpServer


StringOrNumber: TypeAlias = Union[str, int]


@dataclass
class HttpServerBuilder:
    host: str = ""
    port: StringOrNumber = 0
    secret_key: str = ""
    debug: bool = True

    def set_host(self, host: str) -> HttpServerBuilder:
        self.host = host

        return self

    def set_port(self, port: StringOrNumber) -> HttpServerBuilder:
        self.port = port

        return self

    def set_secret_key(self, secret_key: str) -> HttpServerBuilder:
        self.secret_key = secret_key

        return self

    def set_debug(self, debug: bool) -> HttpServerBuilder:
        self.debug = debug

        return self

    def build(self) -> HttpServer:
        return HttpServer(self)
