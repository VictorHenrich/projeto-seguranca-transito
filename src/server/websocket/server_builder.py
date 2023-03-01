from __future__ import annotations
from dataclasses import dataclass
from typing import  Union, TypeAlias
from .server import SocketServer



StringOrNumber: TypeAlias = Union[str, int]


@dataclass
class SocketServerBuilder:
    host: str = ""
    port: StringOrNumber = 0
    secret_key: str = ""
    debug: bool = False

    def set_host(self, host: str) -> SocketServerBuilder:
        self.host = host

        return self

    def set_port(self, port: StringOrNumber) -> SocketServerBuilder:
        self.port = port

        return self

    def set_debug(self, debug: bool) -> SocketServerBuilder:
        self.debug = debug

        return self
    
    def set_secret_key(self, secret_key: str) -> SocketServerBuilder:
        self.secret_key = secret_key

        return self

    def build(self) -> SocketServer:
        return SocketServer(self)
