from typing import Optional
from abc import ABC, abstractmethod
from pika import ConnectionParameters, BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from exceptions import ConnectionAMQPNotDefined


class AbstractAMQP(ABC):
    def __init__(self, connection: Optional[ConnectionParameters]) -> None:
        self.__connection: Optional[ConnectionParameters] = connection

    def get_channel(self) -> BlockingChannel:
        if not self.__connection:
            ConnectionAMQPNotDefined()

        return BlockingConnection(self.__connection).channel()

    @abstractmethod
    def start(self) -> None:
        ...

    @property
    def connection(self) -> Optional[ConnectionParameters]:
        return self.__connection
