from typing import Any, Mapping
from pika import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
import json


from server import App
from server.amqp import AMQPConsumer
from services.integrations import OccurrenceIntegrationProcessService
from patterns.service import IService


QUEUE_OCCURRENCE_INTEGRATION_NAME: str = "queue_occurrences_integration"
EXCHANGE_OCCURRENCE_INTEGRATION_NAME: str = "exchange_occurrence_integration"


@App.amqp.add_consumer(
    "occurrences_integration", QUEUE_OCCURRENCE_INTEGRATION_NAME, ack=True
)
class ConsumerOccurrencesIntegration(AMQPConsumer):
    def __init__(
        self,
        consumer_name: str,
        connection: ConnectionParameters,
        queue_name: str,
        ack: bool,
        arguments: Mapping[str, Any] | None,
    ) -> None:
        super().__init__(consumer_name, connection, queue_name, ack, arguments)

        channel: BlockingChannel = self.get_channel()

        channel.exchange_declare(EXCHANGE_OCCURRENCE_INTEGRATION_NAME)

        channel.queue_declare(QUEUE_OCCURRENCE_INTEGRATION_NAME)

        channel.queue_bind(
            QUEUE_OCCURRENCE_INTEGRATION_NAME, EXCHANGE_OCCURRENCE_INTEGRATION_NAME
        )

    def on_message_queue(self, body: bytes, **kwargs: Any) -> None:
        data: Mapping[str, Any] = json.loads(body)

        occurrence_integration_service: IService[
            None
        ] = OccurrenceIntegrationProcessService(data["occurrence_uuid"])

        occurrence_integration_service.execute()
