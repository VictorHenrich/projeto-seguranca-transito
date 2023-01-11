from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union
from ..http import ServerHttp
from .server import ServerSocket


@dataclass
class ServerSocketBuilder:
    host: Optional[str] = None
    port: Optional[Union[str, int]] = None
    debug: bool = False
    app: Optional[ServerHttp] = None


    def set_host(self, host: str) -> ServerSocketBuilder:
        self.host = host

        return self

    def set_port(self, port: Union[str, int]) -> ServerSocketBuilder:
        self.port = port

        return self

    def set_debug(self, debug: bool) -> ServerSocketBuilder:
        self.debug = debug

        return self

    def set_app(self, app: ServerHttp) -> ServerSocketBuilder:
        self.app = app

        return self

    def build(self) -> ServerSocket:
        return ServerSocket(
            self.app,
            self
        )