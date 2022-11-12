from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from typing import Optional, Union

from .server import ServerHttp


@dataclass
class ServerHttpBuilder(ABC):
    host: Optional[str] = None
    port: Optional[Union[str, int]] = None
    debug: bool = False


    def set_host(self, host: str) -> ServerHttpBuilder:
        self.host = host
        
        return self

    def set_port(self, port: Union[str, int]) -> ServerHttpBuilder:
        self.port = port

        return self

    def set_debug(self, debug: bool) -> ServerHttpBuilder:
        self.debug = debug

        return self

    def build(self) -> ServerHttp:
        return ServerHttp(self)