from typing import Mapping, Any, Optional, TypeAlias
from abc import ABC, abstractmethod
from pika import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import logging

from .abstract_amqp import AbstractAMQP
from exceptions import ConnectionAMQPNotDefined
from utils.types import DictType

ConnectionParamsOptional: TypeAlias = Optional[ConnectionParameters]


class AMQPConsumer(AbstractAMQP, ABC):
    def __init__(
        self,
        consumer_name: str,
        connection: ConnectionParamsOptional,
        queue_name: str,
        ack: bool,
        arguments: Optional[DictType],
    ) -> None:
        super().__init__(connection)

        self.__name: str = consumer_name
        self.__queue_name: str = queue_name
        self.__ack: bool = ack
        self.__arguments: Optional[DictType] = arguments

    @property
    def name(self) -> str:
        return self.__name

    def start(self) -> None:
        if not self.connection:
            raise ConnectionAMQPNotDefined()

        self.on_start()

        channel: BlockingChannel = self.get_channel()

        channel.basic_consume(
            queue=self.__queue_name,
            auto_ack=self.__ack,
            on_message_callback=self.__on_message,
            arguments=self.__arguments,
        )

        logging.info(
            f"Consumer {self.__name} running in {self.connection.host}:{self.connection.port}"
        )

        channel.start_consuming()

    def __on_message(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        options: DictType = {
            "channel": ch,
            "method": method,
            "properties": properties,
        }

        self.on_message_queue(body, **options)

    @abstractmethod
    def on_start(self) -> None:
        pass

    @abstractmethod
    def on_message_queue(self, body: bytes, **kwargs: Any) -> None:
        ...
