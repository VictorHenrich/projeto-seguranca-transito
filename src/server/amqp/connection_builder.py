from __future__ import annotations
from typing import Union
from dataclasses import dataclass
from pika import ConnectionParameters, PlainCredentials


@dataclass
class ConnectionBuilder:
    host: str = ""
    port: Union[str, int] = 5672
    username: str = ""
    password: str = ""

    def set_host(self, host: str) -> ConnectionBuilder:
        self.host = host

        return self

    def set_port(self, port: Union[str, int]) -> ConnectionBuilder:
        self.port = port

        return self

    def set_credentials(self, username: str, password: str) -> ConnectionBuilder:
        self.username = username
        self.password = password

        return self

    def build(self) -> ConnectionParameters:
        return ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=PlainCredentials(
                username=self.username, password=self.password
            ),
        )
