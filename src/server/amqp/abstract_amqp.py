from abc import ABC, abstractmethod
from pika import ConnectionParameters, BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel


class AbstractAMQP(ABC):
    def __init__(self, connection: ConnectionParameters) -> None:
        self.__connection: ConnectionParameters = connection

    def get_channel(self) -> BlockingChannel:
        return BlockingConnection(self.__connection).channel()

    @abstractmethod
    def start(self) -> None:
        ...

    @property
    def connection(self) -> ConnectionParameters:
        return self.__connection