from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union
from ..http import HttpServer
from .server import SocketServer


@dataclass
class ServerSocketBuilder:
    host: Optional[str] = None
    port: Optional[Union[str, int]] = None
    debug: bool = False
    app: Optional[HttpServer] = None

    def set_host(self, host: str) -> ServerSocketBuilder:
        self.host = host

        return self

    def set_port(self, port: Union[str, int]) -> ServerSocketBuilder:
        self.port = port

        return self

    def set_debug(self, debug: bool) -> ServerSocketBuilder:
        self.debug = debug

        return self

    def build(self) -> SocketServer:
        return SocketServer(self)
