from typing import Mapping, Any, Optional, Type
from abc import ABC, abstractmethod
import json
from pika import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from .abstract_amqp import AbstractAMQP


class AMQPConsumer(AbstractAMQP, ABC):
    def __init__(
        self,
        consumer_name: str,
        connection: ConnectionParameters,
        queue_name: str,
        ack: bool,
        arguments: Optional[Mapping[str, Any]],
        data_class: Optional[Type],
    ) -> None:
        super().__init__(connection)

        self.__name: str = consumer_name
        self.__queue_name: str = queue_name
        self.__ack: bool = ack
        self.__arguments: Optional[Mapping[str, Any]] = arguments
        self.__data_class: Optional[Type] = data_class

    @property
    def name(self) -> str:
        return self.__name

    def start(self) -> None:
        channel: BlockingChannel = self.get_channel()

        channel.queue_declare(
            queue=self.__queue_name, durable=True, arguments=self.__arguments
        )

        channel.basic_consume(
            queue=self.__queue_name,
            auto_ack=self.__ack,
            on_message_callback=self.__on_message,
            arguments=self.__arguments,
        )

        print(
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

        payload: Mapping[str, Any] = json.loads(body)

        p: Any = payload if not self.__data_class else self.__data_class(**payload)

        self.on_message_queue(p, **options)

    @abstractmethod
    def on_message_queue(self, body: Any, **kwargs: Mapping[str, Any]) -> None:
        ...