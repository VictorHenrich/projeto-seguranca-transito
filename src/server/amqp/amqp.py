from typing import Optional, Callable, TypeAlias, List
from threading import Thread
from pika import ConnectionParameters

from .consumer import AMQPConsumer
from .publisher import AMQPPublisher
from exceptions import ConnectionAMQPNotDefined
from utils.types import DictType

TypeAMQPConsumer: TypeAlias = type[AMQPConsumer]
ReturnDecoratorAddConsumer: TypeAlias = Callable[[TypeAMQPConsumer], TypeAMQPConsumer]
ConnectionParametersOptional: TypeAlias = Optional[ConnectionParameters]


class AMQPServer:
    __consumers: List[AMQPConsumer] = []

    __default_connection: ConnectionParametersOptional = None

    @classmethod
    def set_default_connection(cls, connection: ConnectionParameters) -> None:
        cls.__default_connection = connection

    @classmethod
    def create_publisher(
        cls,
        publisher_name: str,
        exchange: str,
        body: bytes,
        connection: Optional[ConnectionParameters] = None,
        routing_key: str = "",
        properties: DictType = {"delivery_mode": 2},
    ) -> None:
        connection_: Optional[ConnectionParameters] = (
            connection or cls.__default_connection
        )

        if not connection_:
            raise ConnectionAMQPNotDefined()

        publisher: AMQPPublisher = AMQPPublisher(
            publisher_name,
            connection_,
            exchange,
            body,
            routing_key,
            properties,
        )

        publisher.start()

    @classmethod
    def add_consumer(
        cls,
        consumer_name: str,
        queue_name: str,
        ack: bool = True,
        connection: ConnectionParametersOptional = None,
        arguments: Optional[DictType] = None,
    ) -> ReturnDecoratorAddConsumer:
        def decorator(c: TypeAMQPConsumer) -> TypeAMQPConsumer:
            connection_: Optional[ConnectionParameters] = (
                connection or cls.__default_connection
            )

            consumer: AMQPConsumer = c(
                consumer_name, connection_, queue_name, ack, arguments
            )

            cls.__consumers.append(consumer)

            return c

        return decorator

    @classmethod
    def start_consumers(cls) -> None:
        threads: List[Thread] = [
            Thread(target=consumer.start) for consumer in cls.__consumers
        ]

        [thread.start() for thread in threads]
