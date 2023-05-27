from typing import Mapping, Any, Optional
from abc import ABC, abstractmethod
from pika import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import logging

from .abstract_amqp import AbstractAMQP


class AMQPConsumer(AbstractAMQP, ABC):
    def __init__(
        self,
        consumer_name: str,
        connection: ConnectionParameters,
        queue_name: str,
        ack: bool,
        arguments: Optional[Mapping[str, Any]],
    ) -> None:
        super().__init__(connection)

        self.__name: str = consumer_name
        self.__queue_name: str = queue_name
        self.__ack: bool = ack
        self.__arguments: Optional[Mapping[str, Any]] = arguments

    @property
    def name(self) -> str:
        return self.__name

    def start(self) -> None:
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
        options: Mapping[str, Any] = {
            "channel": ch,
            "method": method,
            "properties": properties,
        }

        self.on_message_queue(body, **options)

    @abstractmethod
    def on_message_queue(self, body: bytes, **kwargs: Any) -> None:
        ...
