from typing import Dict, Optional, Any, Callable, TypeAlias, List, Type
from threading import Thread
from pika import ConnectionParameters

from .consumer import AMQPConsumer
from .publisher import AMQPPublisher


TypeAMQPConsumer: TypeAlias = type[AMQPConsumer]
ReturnDecoratorAddConsumer: TypeAlias = Callable[[TypeAMQPConsumer], TypeAMQPConsumer]
ConnectionParametersOptional: TypeAlias = Optional[ConnectionParameters]


class AMQPServer:
    def __init__(self, default_connection: ConnectionParametersOptional) -> None:
        self.__consumers: Dict[str, AMQPConsumer] = {}
        self.__default_connection: ConnectionParametersOptional = default_connection

    @property
    def default_connection(self) -> ConnectionParametersOptional:
        return self.__default_connection

    def create_publisher(
        self,
        publisher_name: str,
        exchange: str,
        body: Dict[str, Any],
        connection: Optional[ConnectionParameters] = None,
        routing_key: str = "",
        properties: Dict[str, Any] = {"delivery_mode": 2},
    ) -> None:
        connection_: Optional[ConnectionParameters] = (
            connection or self.__default_connection
        )

        if not connection_:
            raise Exception("Connection is not defined!")

        publiser: AMQPPublisher = AMQPPublisher(
            publisher_name,
            connection_,
            exchange,
            body,
            routing_key,
            properties,
        )

        publiser.start()

    def add_consumer(
        self,
        consumer_name: str,
        queue_name: str,
        ack: bool = True,
        connection: ConnectionParametersOptional = None,
        arguments: Optional[Dict[str, Any]] = None,
        data_class: Optional[Type] = None,
    ) -> ReturnDecoratorAddConsumer:
        def decorator(cls: TypeAMQPConsumer) -> TypeAMQPConsumer:
            connection_: Optional[ConnectionParameters] = (
                connection or self.__default_connection
            )

            if not connection_:
                raise Exception("Connection is not defined!")

            consumer: AMQPConsumer = cls(
                consumer_name, connection_, queue_name, ack, arguments, data_class
            )

            self.__consumers[consumer.name] = consumer

            return cls

        return decorator

    def start_consumers(self) -> None:
        threads: List[Thread] = [
            Thread(target=consumer.start) for consumer in self.__consumers.values()
        ]

        [thread.start() for thread in threads]