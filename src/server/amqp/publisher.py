from typing import Union, Mapping, Any
from pika import ConnectionParameters, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
import json
from .abstract_amqp import AbstractAMQP


class AMQPPublisher(AbstractAMQP):
    def __init__(
        self,
        publisher_name: str,
        connection: ConnectionParameters,
        exchange: str,
        body: Mapping[str, Any],
        routing_key: str,
        properties: Mapping[str, Any],
    ) -> None:
        super().__init__(connection)

        self.__publisher_name: str = publisher_name
        self.__exchange: str = exchange
        self.__body: Mapping[str, Any] = body
        self.__routing_key: str = routing_key
        self.__properties: BasicProperties = BasicProperties(**properties)

    def start(self) -> None:
        channel: BlockingChannel = self.get_channel()

        body: bytes = json.dumps(self.__body).encode()

        channel.basic_publish(
            exchange=self.__exchange,
            body=body,
            routing_key=self.__routing_key,
            properties=self.__properties,
        )

        print(f"Publisher {self.__publisher_name} triggered an event!")